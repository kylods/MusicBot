<<<<<<< HEAD
<<<<<<< HEAD
import asyncio
import json
import os
import traceback
import re

from .exceptions import ExtractionError
from .utils import get_header, md5sum


class BasePlaylistEntry:
    def __init__(self):
        self.filename = None
        self.filename_thumbnail = None
=======
=======
>>>>>>> pr/5
import os
import asyncio
import logging
import traceback

from enum import Enum
from .constructs import Serializable
from .exceptions import ExtractionError
from .utils import get_header, md5sum

log = logging.getLogger(__name__)


class EntryTypes(Enum):
    URL = 1
    STEAM = 2
    FILE = 3

    def __str__(self):
        return self.name


class BasePlaylistEntry(Serializable):
    def __init__(self):
        self.filename = None
<<<<<<< HEAD
>>>>>>> pr/5
=======
>>>>>>> pr/5
        self._is_downloading = False
        self._waiting_futures = []

    @property
    def is_downloaded(self):
        if self._is_downloading:
            return False

        return bool(self.filename)

<<<<<<< HEAD
<<<<<<< HEAD
    @classmethod
    def from_json(cls, playlist, jsonstring):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError

=======
>>>>>>> pr/5
=======
>>>>>>> pr/5
    async def _download(self):
        raise NotImplementedError

    def get_ready_future(self):
        """
        Returns a future that will fire when the song is ready to be played. The future will either fire with the result (being the entry) or an exception
        as to why the song download failed.
        """
        future = asyncio.Future()
        if self.is_downloaded:
            # In the event that we're downloaded, we're already ready for playback.
            future.set_result(self)

        else:
            # If we request a ready future, let's ensure that it'll actually resolve at one point.
            asyncio.ensure_future(self._download())
            self._waiting_futures.append(future)

        return future

    def _for_each_future(self, cb):
        """
            Calls `cb` for each future that is not cancelled. Absorbs and logs any errors that may have occurred.
        """
        futures = self._waiting_futures
        self._waiting_futures = []

        for future in futures:
            if future.cancelled():
                continue

            try:
                cb(future)

            except:
                traceback.print_exc()

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)


class URLPlaylistEntry(BasePlaylistEntry):
    def __init__(self, playlist, url, title, duration=0, expected_filename=None, **meta):
        super().__init__()

        self.playlist = playlist
        self.url = url
        self.title = title
        self.duration = duration
        self.expected_filename = expected_filename
        self.meta = meta

        self.download_folder = self.playlist.downloader.download_folder

<<<<<<< HEAD
<<<<<<< HEAD
    @classmethod
    def from_json(cls, playlist, jsonstring):
        data = json.loads(jsonstring)
        print(data)
        # TODO: version check
        url = data['url']
        title = data['title']
        duration = data['duration']
        downloaded = data['downloaded']
        filename = data['filename'] if downloaded else None
        filename_thumbnail = data['filename_thumbnail'] if downloaded else None
        meta = {}

        # TODO: Better [name] fallbacks
        if 'channel' in data['meta']:
            ch = playlist.bot.get_channel(data['meta']['channel']['id'])
            meta['channel'] = ch or data['meta']['channel']['name']

        if 'author' in data['meta']:
            meta['author'] = meta['channel'].server.get_member(data['meta']['author']['id'])

        return cls(playlist, url, title, duration, filename, **meta)

    def to_json(self):
        data = {
            'version': 1,
            'type': self.__class__.__name__,
=======
    def __json__(self):
        return self._enclose_json({
            'version': 1,
>>>>>>> pr/5
=======
    def __json__(self):
        return self._enclose_json({
            'version': 1,
>>>>>>> pr/5
            'url': self.url,
            'title': self.title,
            'duration': self.duration,
            'downloaded': self.is_downloaded,
<<<<<<< HEAD
<<<<<<< HEAD
            'filename': self.filename,
            'filename_thumbnail': self.filename_thumbnail,
            'meta': {
                i: {
                    'type': self.meta[i].__class__.__name__,
                    'id': self.meta[i].id,
                    'name': self.meta[i].name
                    } for i in self.meta
                }
            # Actually I think I can just getattr instead, getattr(discord, type)
        }
        return json.dumps(data, indent=2)
=======
=======
>>>>>>> pr/5
            'expected_filename': self.expected_filename,
            'filename': self.filename,
            'full_filename': os.path.abspath(self.filename) if self.filename else self.filename,
            'meta': {
                name: {
                    'type': obj.__class__.__name__,
                    'id': obj.id,
                    'name': obj.name
                } for name, obj in self.meta.items() if obj
            }
        })

    @classmethod
    def _deserialize(cls, data, playlist=None):
        assert playlist is not None, cls._bad('playlist')

        try:
            # TODO: version check
            url = data['url']
            title = data['title']
            duration = data['duration']
            downloaded = data['downloaded']
            filename = data['filename'] if downloaded else None
            expected_filename = data['expected_filename']
            meta = {}

            # TODO: Better [name] fallbacks
            if 'channel' in data['meta']:
                meta['channel'] = playlist.bot.get_channel(data['meta']['channel']['id'])

            if 'author' in data['meta']:
                meta['author'] = meta['channel'].server.get_member(data['meta']['author']['id'])

            entry = cls(playlist, url, title, duration, expected_filename, **meta)
            entry.filename = filename

            return entry
        except Exception as e:
            log.error("Could not load {}".format(cls.__name__), exc_info=e)
<<<<<<< HEAD
>>>>>>> pr/5
=======
>>>>>>> pr/5

    # noinspection PyTypeChecker
    async def _download(self):
        if self._is_downloading:
            return

        self._is_downloading = True
        try:
            # Ensure the folder that we're going to move into exists.
            if not os.path.exists(self.download_folder):
                os.makedirs(self.download_folder)

            # self.expected_filename: audio_cache\youtube-9R8aSKwTEMg-NOMA_-_Brain_Power.m4a
            extractor = os.path.basename(self.expected_filename).split('-')[0]

            # the generic extractor requires special handling
            if extractor == 'generic':
<<<<<<< HEAD
<<<<<<< HEAD
                # print("Handling generic")
                # remove thumbnail images from list
                imgPattern = re.compile('(\.(jpg|jpeg|png|gif|bmp))$', flags=re.IGNORECASE)
                flistdir = [f.rsplit('-', 1)[0] for f in os.listdir(self.download_folder) if not imgPattern.search(f)]
=======
                flistdir = [f.rsplit('-', 1)[0] for f in os.listdir(self.download_folder)]
>>>>>>> pr/5
=======
                flistdir = [f.rsplit('-', 1)[0] for f in os.listdir(self.download_folder)]
>>>>>>> pr/5
                expected_fname_noex, fname_ex = os.path.basename(self.expected_filename).rsplit('.', 1)

                if expected_fname_noex in flistdir:
                    try:
                        rsize = int(await get_header(self.playlist.bot.aiosession, self.url, 'CONTENT-LENGTH'))
                    except:
                        rsize = 0

                    lfile = os.path.join(
                        self.download_folder,
                        os.listdir(self.download_folder)[flistdir.index(expected_fname_noex)]
                    )

                    # print("Resolved %s to %s" % (self.expected_filename, lfile))
                    lsize = os.path.getsize(lfile)
                    # print("Remote size: %s Local size: %s" % (rsize, lsize))

                    if lsize != rsize:
                        await self._really_download(hash=True)
                    else:
                        # print("[Download] Cached:", self.url)
                        self.filename = lfile

                else:
                    # print("File not found in cache (%s)" % expected_fname_noex)
                    await self._really_download(hash=True)

            else:
<<<<<<< HEAD
<<<<<<< HEAD
                imgPattern = re.compile('(\.(jpg|jpeg|png|gif|bmp))$', flags=re.IGNORECASE)
                ldir = [f for f in os.listdir(self.download_folder) if not imgPattern.search(f)]
=======
                ldir = os.listdir(self.download_folder)
>>>>>>> pr/5
=======
                ldir = os.listdir(self.download_folder)
>>>>>>> pr/5
                flistdir = [f.rsplit('.', 1)[0] for f in ldir]
                expected_fname_base = os.path.basename(self.expected_filename)
                expected_fname_noex = expected_fname_base.rsplit('.', 1)[0]

                # idk wtf this is but its probably legacy code
                # or i have youtube to blame for changing shit again

                if expected_fname_base in ldir:
                    self.filename = os.path.join(self.download_folder, expected_fname_base)
<<<<<<< HEAD
<<<<<<< HEAD
                    print("[Download] Cached:", self.url)

                elif expected_fname_noex in flistdir:
                    print("[Download] Cached (different extension):", self.url)
                    self.filename = os.path.join(self.download_folder, ldir[flistdir.index(expected_fname_noex)])
                    print("Expected %s, got %s" % (
                        self.expected_filename.rsplit('.', 1)[-1],
                        self.filename.rsplit('.', 1)[-1]
                    ))

=======
=======
>>>>>>> pr/5
                    log.info("Download cached: {}".format(self.url))

                elif expected_fname_noex in flistdir:
                    log.info("Download cached (different extension): {}".format(self.url))
                    self.filename = os.path.join(self.download_folder, ldir[flistdir.index(expected_fname_noex)])
                    log.debug("Expected {}, got {}".format(
                        self.expected_filename.rsplit('.', 1)[-1],
                        self.filename.rsplit('.', 1)[-1]
                    ))
<<<<<<< HEAD
>>>>>>> pr/5
=======
>>>>>>> pr/5
                else:
                    await self._really_download()

            # Trigger ready callbacks.
            self._for_each_future(lambda future: future.set_result(self))

        except Exception as e:
            traceback.print_exc()
            self._for_each_future(lambda future: future.set_exception(e))

        finally:
            self._is_downloading = False

    # noinspection PyShadowingBuiltins
    async def _really_download(self, *, hash=False):
<<<<<<< HEAD
<<<<<<< HEAD
        print("[Download] Started: '%s' [s%]" % (self.title, self.url)
=======
        log.info("Download started: {}".format(self.url))
>>>>>>> pr/5
=======
        log.info("Download started: {}".format(self.url))
>>>>>>> pr/5

        try:
            result = await self.playlist.downloader.extract_info(self.playlist.loop, self.url, download=True)
        except Exception as e:
            raise ExtractionError(e)

<<<<<<< HEAD
<<<<<<< HEAD
        print("[Download] Complete: '%s' [%s]" % (self.title, self.url))

        if result is None:
=======
=======
>>>>>>> pr/5
        log.info("Download complete: {}".format(self.url))

        if result is None:
            log.critical("YTDL has failed, everyone panic")
<<<<<<< HEAD
>>>>>>> pr/5
=======
>>>>>>> pr/5
            raise ExtractionError("ytdl broke and hell if I know why")
            # What the fuck do I do now?

        self.filename = unhashed_fname = self.playlist.downloader.ytdl.prepare_filename(result)

<<<<<<< HEAD
<<<<<<< HEAD
        # Search for file name with an image suffix
        imgPattern = re.compile(self.filename.lstrip(self.download_folder + os.sep).rsplit('.', 1)[0] + '(\.(jpg|jpeg|png|gif|bmp))$', re.IGNORECASE)
        self.filename_thumbnail = next(os.path.join(self.download_folder, f) for f in os.listdir(self.download_folder) if imgPattern.search(f))

=======
>>>>>>> pr/5
=======
>>>>>>> pr/5
        if hash:
            # insert the 8 last characters of the file hash to the file name to ensure uniqueness
            self.filename = md5sum(unhashed_fname, 8).join('-.').join(unhashed_fname.rsplit('.', 1))

            if os.path.isfile(self.filename):
                # Oh bother it was actually there.
                os.unlink(unhashed_fname)
            else:
                # Move the temporary file to it's final location.
                os.rename(unhashed_fname, self.filename)


<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> pr/5
class StreamPlaylistEntry(BasePlaylistEntry):
    def __init__(self, playlist, url, title, *, destination=None, **meta):
        super().__init__()

        self.playlist = playlist
        self.url = url
        self.title = title
        self.destination = destination
        self.duration = 0
        self.meta = meta

        if self.destination:
            self.filename = self.destination

    def __json__(self):
        return self._enclose_json({
            'version': 1,
            'url': self.url,
            'filename': self.filename,
            'title': self.title,
            'destination': self.destination,
            'meta': {
                name: {
                    'type': obj.__class__.__name__,
                    'id': obj.id,
                    'name': obj.name
                } for name, obj in self.meta.items() if obj
            }
        })

    @classmethod
    def _deserialize(cls, data, playlist=None):
        assert playlist is not None, cls._bad('playlist')

        try:
            # TODO: version check
            url = data['url']
            title = data['title']
            destination = data['destination']
            filename = data['filename']
            meta = {}

            # TODO: Better [name] fallbacks
            if 'channel' in data['meta']:
                ch = playlist.bot.get_channel(data['meta']['channel']['id'])
                meta['channel'] = ch or data['meta']['channel']['name']

            if 'author' in data['meta']:
                meta['author'] = meta['channel'].server.get_member(data['meta']['author']['id'])

            entry = cls(playlist, url, title, destination=destination, **meta)
            if not destination and filename:
                entry.filename = destination

            return entry
        except Exception as e:
            log.error("Could not load {}".format(cls.__name__), exc_info=e)

    # noinspection PyMethodOverriding
    async def _download(self, *, fallback=False):
        self._is_downloading = True

        url = self.destination if fallback else self.url

        try:
            result = await self.playlist.downloader.extract_info(self.playlist.loop, url, download=False)
        except Exception as e:
            if not fallback and self.destination:
                return await self._download(fallback=True)

            raise ExtractionError(e)
        else:
            self.filename = result['url']
            # I might need some sort of events or hooks or shit
            # for when ffmpeg inevitebly fucks up and i have to restart
            # although maybe that should be at a slightly lower level
        finally:
            self._is_downloading = False
<<<<<<< HEAD
>>>>>>> pr/5
=======
>>>>>>> pr/5
