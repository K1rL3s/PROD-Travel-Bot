from core.repositories import NoteRepo


class NoteService:
    def __init__(self, note_repo: NoteRepo) -> None:
        self.note_repo = note_repo
