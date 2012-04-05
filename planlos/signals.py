# coding: utf-8


from blinker import Namespace

planlos_signals = Namespace()

user_requested = planlos_signals.signal('user-requested')
user_removed = planlos_signals.signal('user-removed')
