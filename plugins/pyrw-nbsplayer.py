import os
import time
import traceback
from dataclasses import dataclass
from pathlib import Path

import mc  # pyright: reportMissingImports=false
import pynbs

PLUGIN_NAME = "PyrWNbsPlayer"

DATA_PATH = Path.cwd() / "plugins" / PLUGIN_NAME
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True, exist_ok=True)

BUILTIN_INST = {
    0: "note.harp",
    1: "note.bassattack",
    2: "note.bd",
    3: "note.snare",
    4: "note.hat",
    5: "note.guitar",
    6: "note.flute",
    7: "note.bell",
    8: "note.chime",
    9: "note.xylobone",
    10: "note.iron_xylophone",
    11: "note.cow_bell",
    12: "note.didgeridoo",
    13: "note.bit",
    14: "note.banjo",
    15: "note.pling",
}


@dataclass()
class ProcessedNote:
    time: int
    name: str
    volume: float
    pitch: float


@dataclass()
class PlayTask:
    start_time: int
    title: str
    length: int
    notes: list[ProcessedNote]
    len_str: str
    progress: float = -1.0


play_tasks: dict[str, PlayTask] = {}


def stop_play(xuid: str):
    if xuid in play_tasks:
        del play_tasks[xuid]

        try:
            player = mc.getPlayerByXuid(xuid)
            player.removeBossBar()
        except BaseException:
            pass


def get_timestamp() -> int:
    return int(time.time() * 1000)


def parse_nbs(nbs: pynbs.File) -> tuple[list[ProcessedNote], float]:
    header: pynbs.Header = nbs.header
    notes: list[pynbs.Note] = nbs.notes
    instruments: list[pynbs.Instrument] = nbs.instruments
    layers: list[pynbs.Layer] = nbs.layers

    time_per_tick = 20 / header.tempo * 50

    processed: list[ProcessedNote] = []
    for note in notes:
        layer = layers[note.layer]

        time = int(note.tick * time_per_tick)
        sound_name = BUILTIN_INST.get(note.instrument)
        inst_pitch = 45
        if not sound_name:
            inst = [x for x in instruments if x.id == note.instrument]
            if inst:
                inst = inst[0]
                sound_name = os.path.splitext(inst.file)[0]
                inst_pitch = inst.pitch
            else:
                sound_name = BUILTIN_INST[0]

        volume = (note.velocity / 100) * (layer.volume / 100)

        final_key = note.key + (inst_pitch - 45) + note.pitch / 100
        pitch = 2 ** ((final_key - 45) / 12)

        processed.append(ProcessedNote(time, sound_name, volume, pitch))

    return processed, time_per_tick


def format_time(time_ms: int) -> str:
    sec, ms = divmod(time_ms, 1000)
    minute, sec = divmod(sec, 60)
    return f"{minute}:{sec:0>2d}.{str(ms).zfill(3)[0]}"


def execute_task(xuid: str, task: PlayTask):
    try:
        player = mc.getPlayerByXuid(xuid)
    except BaseException:
        stop_play(xuid)
        return

    time_now = get_timestamp()
    time_passed = time_now - task.start_time

    progress = 0.0
    if time_passed:
        progress = round(time_passed / task.length, 2)
    task.progress = progress

    title = f"§e{format_time(time_passed)} §7| {task.title} §7| §6{task.len_str}"
    player.removeBossBar()
    player.setBossBar(title, progress)

    pos: list[float] = player.pos
    x, y, z = pos

    while task.notes:
        note = task.notes[0]
        if note.time > time_passed:
            break
        task.notes.pop(0)
        player.sendPlaySoundPacket(note.name, x, y, z, note.volume, note.pitch)

    if not task.notes:
        stop_play(xuid)


def on_tick(_):
    # prevent dictionary changed size during iteration
    for xuid, task in play_tasks.copy().items():
        execute_task(xuid, task)


def play_nbs(xuid: str, nbs: pynbs.File):
    if xuid in play_tasks:
        stop_play(xuid)

    header: pynbs.Header = nbs.header

    parsed_notes, time_per_tick = parse_nbs(nbs)
    total_len = round(header.song_length * time_per_tick)

    name = header.song_name or header.song_origin or "未知"
    author = header.original_author or header.song_author or "未知"
    title = f"§dPyrWNbsPlayer §7| §b{name} §f- §3{author}"

    task = PlayTask(
        get_timestamp(),
        title,
        total_len,
        parsed_notes,
        format_time(total_len),
    )
    play_tasks[xuid] = task


def nbs_cmd(data: dict):
    cmd: str = data["cmd"]
    player = data["player"]

    if not (cmd == "/nbs" or cmd.startswith("/nbs ")):
        return

    arg = cmd.removeprefix("/nbs").strip().removeprefix('"').removesuffix('"')

    if not arg:
        player.sendTextPacket("§c命令用法: /nbs <文件名>")
        return False

    file = DATA_PATH / arg
    if not file.exists():
        player.sendTextPacket("§c文件不存在")
        return False

    try:
        nbs = pynbs.read(str(file))
    except BaseException:
        exc = traceback.format_exc()
        player.sendTextPacket(f"§c打开文件失败！\n{exc}")
        return False

    xuid: str = player.xuid
    play_nbs(xuid, nbs)

    return False


def nbstop_cmd(player):
    stop_play(player.xuid)
    player.sendTextPacket("停止播放")


mc.setListener("onTick", on_tick)
mc.setListener("onInputCommand", nbs_cmd)
mc.setCommandDescription("nbs", PLUGIN_NAME)
mc.setCommandDescription("nbstop", PLUGIN_NAME, nbstop_cmd)
