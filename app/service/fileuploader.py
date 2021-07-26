import os
from pathlib import Path
from uuid import uuid4

from starlette.datastructures import UploadFile

from app.service.errorhandler import ApplicationError


class FileUploader:
    def __init__(
            self,
            file: UploadFile,
    ):
        self.file = file
        self.size = 0

    @property
    def filename(self):
        return self.file.filename

    @property
    def extension(self):
        try:
            rs = self.filename.rsplit('.', 1)
            return rs[1].lower()
        except:
            return ''

    @property
    def name_only(self):
        try:
            rs = self.filename.rsplit('.', 1)
            return rs[0]
        except:
            return ''

    @property
    def mimetype(self):
        return self.file.content_type

    @property
    def file_type(self):
        return self.mimetype.split('/')[0].upper()

    async def save(self, folder: Path, save_name=None, is_name_random=True, buffer_size=1024 * 1024):
        if not os.path.exists(folder):
            os.makedirs(folder)

        if is_name_random:
            dst = folder.joinpath(f'{uuid4().hex}.{self.extension}')
        else:
            dst = folder.joinpath(save_name or self.filename)

        with open(dst, 'wb') as out_file:
            while True:
                chunk = await self.file.read(buffer_size)
                if chunk:
                    out_file.write(chunk)
                else:
                    await self.file.close()
                    break

        self.size = dst.stat().st_size
        return dst

    def __nonzero__(self):
        return bool(self.filename)

    __bool__ = __nonzero__

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.filename} ({self.mimetype})>"
