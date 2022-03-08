#!/usr/bin/env python
import argparse
import datetime
import errno
import sys

from bsm import Manager, Episode


def valid_date(s):
  try:
    return datetime.date.fromisoformat(s)
  except ValueError:
    msg = "not a valid date: {0!r}".format(s)
    raise argparse.ArgumentTypeError(msg)


def valid_time(s):
  try:
    return datetime.time.fromisoformat(s)
  except ValueError:
    msg = "not a valid time: {0!r}".format(s)
    raise argparse.ArgumentTypeError(msg)


def call_uploader_with_args():
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
  parser.add_argument("--audio",
                      help="input audio filename", required=True)
  parser.add_argument("--title",
                      help="title of the podcast", required=True)
  parser.add_argument("--description",
                      help="description of the podcast", required=True)
  parser.add_argument("--tags", nargs='*',
                      help="tags for the episode", required=False)
  parser.add_argument("--publish-at-date", type=valid_date,
                      help="date to publish the podcast", required=False)
  parser.add_argument("--publish-at-time", type=valid_time, required=False,
                      help="time to publish the podcast")
  parser.add_argument("--episode-number", type=int, required=False,
                      help="episode number of podcast (if none, most recent ep number +1)")
  parser.add_argument("--season-number", type=int, required=False,
                      help="season number of podcast (if none, season number of most recent episode")
  parser.add_argument("--private", type=bool, default=False,
                      help="whether or not podcast is private", required=False)
  parser.add_argument("--explicit", type=bool, default=False,
                      help="whether or not podcast is explicit", required=False)
  parser.add_argument("--email-after-process", type=bool, default=True,
                      help="whether or not to email after the processing is done", required=False)
  parser.add_argument("--api-key",
                      help="API key to use when calling Buzzsprout", required=True)
  parser.add_argument("--podcast-id",
                      help="ID of podcast to upload to", required=True)

  args, _ = parser.parse_known_args()

  # Compile the publish time if applicable
  publish_at = None
  if (args.publish_at_date is not None and args.publish_at_time is None) or \
     (args.publish_at_date is None and args.publish_at_time is not None):
     exit("Must specify both publish_at date and time for scheduling")

  if args.publish_at_date is not None:
    publish_at = datetime.datetime.combine(args.publish_at_date, args.publish_at_time)
  
  if publish_at < datetime.datetime.now():
    exit("Must specify a time in the future")

  upload_podcast(args.audio, args.title, args.description, args.tags, publish_at,
                      args.episode_number, args.season_number, args.private, args.explicit, 
                      args.email_after_process, args.api_key, args.podcast_id)


def upload_podcast(audio, title, description, tags, publish_at, episode_number, season_number,
                        private, explicit, email_after_process, api_key, podcast_id):
  manager = Manager(podcast_id, api_key)
  
  (default_ep_num, default_season_num) = get_default_episode_values(manager)
  episode = Episode(
    title = title,
    description = description,
    tags = ",".join(tags) if tags is not None else "",
    published_at = publish_at.isoformat() if publish_at is not None else None,
    episode_number = episode_number if episode_number is not None else default_ep_num,
    season_number = season_number if season_number is not None else default_season_num,
    explicit = explicit,
    private = "true" if private else "false",
    email_user_after_audio_processed = email_after_process
  )

  new_episode = manager.post_episode(episode = episode, audio_file = audio)
  print(new_episode)

def get_default_episode_values(manager):
  newest = manager.get_all_episodes().newest()
  return (newest.episode_number + 1, newest.season_number)


if __name__ == "__main__":
  try:
    call_uploader_with_args()
  except KeyboardInterrupt:
    # The user asked the program to exit
    sys.exit(1)
  except IOError as e:
    # When this program is used in a shell pipeline and an earlier program in
    # the pipeline is terminated, we'll receive an EPIPE error.  This is normal
    # and just an indication that we should exit after processing whatever
    # input we've received -- we don't consume standard input so we can just
    # exit cleanly in that case.
    if e.errno != errno.EPIPE:
      raise

    # We still exit with a non-zero exit code though in order to propagate the
    # error code of the earlier process that was terminated.
    sys.exit(1)

  sys.exit(0)