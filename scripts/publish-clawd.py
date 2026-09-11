#!/usr/bin/env python3
"""Publish the two explicitly authorized Clawd films; private upload before served-4K verification.

Credentials and resumable-session receipts stay outside Git. This command does
not create playlists, replace existing films, or upload an uncertain attempt twice.
"""
import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parents[1]
CHANNEL = 'UCg0cw2ouRhQ8dr114yGp0mA'
PLAYLIST = 'PLMhsxBEsgHFU'
PLAYLIST_TITLE = 'CSYE 7270 Virtual Environments and Real-Time 3D'
SHARED = '''
Professor Bear is doing Assignment 1 alongside the class. This is iteration one, not a finished assignment: change the main character to Clawd while preserving the starter level and mechanics. Task mini-goals, the final agentic-loop goal, new hazards, and the required level extension come later.

Start early. Make one improvement, inspect it, then make another improvement or test next session. A failed attempt is useful evidence when you record what it ruled out. Keep an honest Frictional log and identify human and AI contributions. Do not invent days of work or tests you never performed.

GAME AND SOURCES
Clawd project: https://github.com/nikbearbrown/walker-jumpman-clawd
Original starter: https://github.com/nikbearbrown/walker-jumpman
Walker: https://github.com/nikbearbrown/walker
Brutalist: https://github.com/nikbearbrown/brutalist.art
Course playlist: https://www.youtube.com/playlist?list=PLMhsxBEsgHFU
AI Policy for Professor Bear's Courses: https://youtu.be/8Ut0Cdl6vMw

EVIDENCE AND LIMITS
Actual Godot output uses scripted normal keyboard and mouse inputs, not a human playtest. Gallery and collision-reference views are labeled diagnostic demonstrations. Replayed footage is identified as the same captured take, not a new test. The wider arms still extend beyond the unchanged collider. Human judgment is needed to decide readability, fairness, and the next revision.

PRODUCTION
Liam is an AI narrator using local Kokoro speech synthesis, not a recording or clone of Professor Bear. Suggested Claude prompts and Godot editor reconstructions are labeled. Native 3840 x 2160, 30 fps landscape master, optional English closed captions, no burned-in captions. Regular Brutalist outro. Clawd/Claude are associated with Anthropic; this is an independent educational project, not an official Anthropic or Godot product.

#CSYE7270 #Godot #Clawd #WalkerGameAI #GameDevelopment #ClaudeCode
'''
PROFILES = {
    'walkthrough': {
        'title': 'Clawd in Walker Jumpman: First Playthrough | CSYE 7270',
        'description': 'See Clawd move, jump, fail, retry, pause, and finish in the existing Walker Jumpman level. Liam walks through one focused character change, then shows all 18 animation previews. Built with Brutalist godot-waikthrough walker and riff.\n' + SHARED,
    },
    'gamedev': {
        'title': 'Building Clawd: Code to Gameplay, One Change at a Time | CSYE 7270',
        'description': 'Trace seven exact source excerpts directly to their visible results in Godot: Clawd geometry, state selection, movement and collision, jumping, pause, finish, and the animation gallery. Liam explains the separation between character art and unchanged game mechanics. Built with Brutalist godot-gamedev walker.\n' + SHARED,
    },
}

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    os.replace(temp, path)

def items(y, playlist):
    rows, token = [], None
    while True:
        result = y.playlistItems().list(part='snippet', playlistId=playlist, maxResults=50, pageToken=token).execute()
        rows.extend(result.get('items', []))
        token = result.get('nextPageToken')
        if not token:
            return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('film', choices=PROFILES)
    parser.add_argument('action', choices=['upload', 'status', 'captions', 'publish'])
    args = parser.parse_args()
    profile = PROFILES[args.film]
    slug = 'claude-liam-walker-jumpman-clawd-' + args.film
    reel = ROOT / 'youtube' / slug
    master = reel / 'exports/landscape' / (slug + '.mp4')
    ledger = reel / '_publish/receipt.json'
    receipt = json.loads(ledger.read_text()) if ledger.exists() else {}
    credential_path = os.environ.get('CLAWD_YOUTUBE_CREDENTIALS', str(ROOT.parent / 'youtube/credentials/nikbearbrown/token.json'))
    credentials = Credentials.from_authorized_user_file(credential_path)
    if not credentials.valid:
        credentials.refresh(Request())
    y = build('youtube', 'v3', credentials=credentials, cache_discovery=False)
    channels = y.channels().list(part='snippet,contentDetails', mine=True).execute()['items']
    if [c['id'] for c in channels] != [CHANNEL]:
        raise RuntimeError('Authenticated channel is not Nik Bear Brown')
    playlist = y.playlists().list(part='snippet,status', id=PLAYLIST).execute()['items'][0]
    if playlist['snippet']['channelId'] != CHANNEL or playlist['snippet']['title'] != PLAYLIST_TITLE:
        raise RuntimeError('Existing course playlist identity mismatch')

    if args.action == 'upload':
        if receipt:
            raise RuntimeError('Existing upload receipt: reconcile rather than duplicate')
        recent = y.playlistItems().list(part='snippet', playlistId=channels[0]['contentDetails']['relatedPlaylists']['uploads'], maxResults=50).execute().get('items', [])
        if any(r['snippet']['title'] == profile['title'] for r in recent):
            raise RuntimeError('Matching existing video title: inspect instead of reuploading')
        qc = json.loads((reel / 'evidence/final-render.json').read_text())
        digest = sha(master)
        if not all(qc.get(k) for k in ('compile_passed', 'audio_preservation_passed', 'ai_visual_review_complete', 'publication_authorized')) or qc['master_sha256'] != digest:
            raise RuntimeError('Hash-bound render review or publication authorization missing')
        metadata = {**profile, 'tags': ['CSYE 7270', 'Godot', 'Walker', 'walker-jumpman-clawd', 'Clawd', 'Claude Code', 'GDScript', 'game development', 'Frictional', 'Brutalist', 'Nik Bear Brown'], 'categoryId': '27', 'defaultLanguage': 'en', 'defaultAudioLanguage': 'en'}
        receipt = {'state': 'upload-started', 'started_at': now(), 'master_sha256': digest, 'channel_id': CHANNEL, 'playlist_id': PLAYLIST, 'metadata': metadata, 'authorization': 'User requested both 4K films published to the CSYE 7270 playlist.'}
        save(ledger, receipt)
        request = y.videos().insert(part='snippet,status', body={'snippet': metadata, 'status': {'privacyStatus': 'private', 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}, media_body=MediaFileUpload(str(master), mimetype='video/mp4', chunksize=8*1024*1024, resumable=True), notifySubscribers=True)
        response = None
        while response is None:
            progress, response = request.next_chunk(num_retries=3)
            if request.resumable_uri:
                receipt['resumable_uri'] = request.resumable_uri
                save(ledger, receipt)
            if progress:
                print(f'{args.film}: {progress.progress():.0%}', flush=True)
        receipt.update(video_id=response['id'], state='uploaded-private', uploaded_at=now())
        save(ledger, receipt)
        print('Uploaded private: https://www.youtube.com/watch?v=' + response['id'])
        return

    vid = receipt.get('video_id')
    if not vid:
        raise RuntimeError('No confirmed video ID; inspect uncertain upload')
    video = y.videos().list(part='snippet,status,processingDetails,fileDetails', id=vid).execute()['items'][0]
    if video['snippet']['channelId'] != CHANNEL:
        raise RuntimeError('Video owner mismatch')
    if args.action == 'status':
        print(json.dumps({'video_id': vid, 'title': video['snippet']['title'], 'status': video['status'], 'processing': video.get('processingDetails'), 'streams': video.get('fileDetails', {}).get('videoStreams')}, indent=2))
        return
    if args.action == 'captions':
        subtitle = master.with_suffix('.srt')
        if not subtitle.exists():
            raise RuntimeError('Aligned SRT missing')
        existing = [c for c in y.captions().list(part='snippet', videoId=vid).execute().get('items', []) if c['snippet'].get('language') == 'en' and c['snippet'].get('trackKind') != 'ASR']
        if existing:
            receipt['caption_id'] = existing[0]['id']
            save(ledger, receipt)
            print('English caption track already exists; not duplicating')
            return
        if receipt.get('caption_attempt_started'):
            raise RuntimeError('Uncertain caption attempt: reconcile before retry')
        receipt['caption_attempt_started'] = now()
        save(ledger, receipt)
        result = y.captions().insert(part='snippet', body={'snippet': {'videoId': vid, 'language': 'en', 'name': 'English', 'isDraft': False}}, media_body=MediaFileUpload(str(subtitle), mimetype='application/x-subrip')).execute()
        receipt.update(caption_id=result['id'], caption_sha256=sha(subtitle))
        save(ledger, receipt)
        print('English caption track uploaded')
        return

    if video.get('processingDetails', {}).get('processingStatus') != 'succeeded':
        raise RuntimeError('YouTube processing is not finished')
    if not any(s.get('widthPixels') == 3840 and s.get('heightPixels') == 2160 for s in video.get('fileDetails', {}).get('videoStreams', [])):
        raise RuntimeError('YouTube source resolution is not confirmed 4K')
    served = json.loads((reel / '_publish/youtube-4k.json').read_text())
    if served.get('video_id') != vid or served.get('quality') != '2160p 4K':
        raise RuntimeError('Browser verification of served 4K is missing')
    if not receipt.get('caption_id') or sha(master) != receipt['master_sha256']:
        raise RuntimeError('Caption confirmation missing or master changed')
    rows = items(y, PLAYLIST)
    found = [r for r in rows if r['snippet']['resourceId']['videoId'] == vid]
    if len(found) > 1:
        raise RuntimeError('Duplicate playlist entries require inspection')
    if not found:
        if receipt.get('playlist_insert_started') or receipt.get('playlist_item_id'):
            raise RuntimeError('Playlist insertion already attempted; wait for visibility or reconcile, never duplicate')
        if args.film == 'gamedev':
            first = ROOT / 'youtube/claude-liam-walker-jumpman-clawd-walkthrough/_publish/receipt.json'
            earlier = json.loads(first.read_text())
            if earlier.get('state') != 'published' or not any(r['snippet']['resourceId']['videoId'] == earlier.get('video_id') for r in rows):
                raise RuntimeError('Publish walkthrough before gamedev')
        receipt['playlist_insert_started'] = now()
        save(ledger, receipt)
        result = y.playlistItems().insert(part='snippet', body={'snippet': {'playlistId': PLAYLIST, 'resourceId': {'kind': 'youtube#video', 'videoId': vid}}}).execute()
        receipt['playlist_item_id'] = result['id']
        save(ledger, receipt)
    if video['status']['privacyStatus'] != 'public':
        y.videos().update(part='status', body={'id': vid, 'status': {'privacyStatus': 'public', 'license': video['status'].get('license', 'youtube'), 'embeddable': True, 'publicStatsViewable': True, 'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}}).execute()
    for attempt in range(5):
        check = y.videos().list(part='status', id=vid).execute()['items'][0]
        rows = items(y, PLAYLIST)
        found = [r for r in rows if r['snippet']['resourceId']['videoId'] == vid]
        if check['status']['privacyStatus'] == 'public' and len(found) == 1:
            break
        if attempt < 4:
            time.sleep(2)
    if check['status']['privacyStatus'] != 'public' or len(found) != 1:
        raise RuntimeError('Publication/membership verification incomplete; inspect without duplicating')
    receipt.update(state='published', published_at=now(), playlist_position=found[0]['snippet']['position']+1, served_4k=served)
    save(ledger, receipt)
    public = {k: receipt[k] for k in ('state', 'video_id', 'master_sha256', 'channel_id', 'playlist_id', 'playlist_position', 'published_at', 'caption_id', 'served_4k')}
    save(reel / 'evidence/publication.json', public)
    print('Published https://www.youtube.com/watch?v=' + vid)

if __name__ == '__main__':
    main()
