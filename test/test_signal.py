from read_signal import Signal, Direction
import pytest


def test_pump():
    text = ''''┌ 📈 PUMP: #SKLUSDT 🚀🚀🚀
    ├ 🟢 CHANGE: +5.22% 🥳
    ┊  ┌ ₮ 0.10469
    ┊  ┊  ⇧
    ┊  └ ₮ 0.0995
    ├ ⏰ Time Δ: 252.69 sec.
    └ ⚙️ 5.0% per 300.0 sec.'''
    new_signal = Signal(text)

    assert new_signal.direction == Direction.PUMP
    assert new_signal.symbol == 'SKLUSDT'
    assert new_signal.high_sum == '0.10469'
    assert new_signal.low_sum == '0.0995'

def test_dump():
    text = '''┌ 📉 DUMP: #XAIUSDT 😱😱😱
    ├ 🔴 CHANGE: -5.26% 😡
    ┊  ┌ ₮ 0.6792
    ┊  ┊   ⇩
    ┊  └ ₮ 0.6435
    ├ ⏰ Time Δ: 283.58 sec.
    └ ⚙️ 5.0% per 300.0 sec.'''
    new_signal = Signal(text)

    assert new_signal.direction == Direction.DUMP
    assert new_signal.symbol == 'XAIUSDT'
    assert new_signal.high_sum == '0.6792'
    assert new_signal.low_sum == '0.6435'
