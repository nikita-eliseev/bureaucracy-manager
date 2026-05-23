import enum


class TaskStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    needs_attention = "needs_attention"
    done = "done"