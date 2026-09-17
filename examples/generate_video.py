"""
Text-to-video generation via Higgsfield API (bytedance/seedance-2.5/text-to-video).

Requires HF_KEY (or HF_API_KEY + HF_API_SECRET) in the environment.
Usage: python examples/generate_video.py "your prompt here"
"""
import sys
import time

import higgsfield_client
from higgsfield_client import CredentialsMissedError, HiggsfieldClientError

ENDPOINT = "bytedance/seedance-2.5/text-to-video"

DEFAULT_ARGUMENTS = {
    "resolution": "720p",
    "generate_audio": True,
    "duration": 5,
    "aspect_ratio": "16:9",
    "output_format": "mp4",
}


def generate_video(prompt: str, **overrides) -> dict:
    """Submit a request and poll until it reaches a terminal state.

    Returns the raw result dict. Raises HiggsfieldClientError on
    failure/NSFW/cancelled terminal states or transport errors.
    """
    arguments = {"prompt": prompt, **DEFAULT_ARGUMENTS, **overrides}
    controller = higgsfield_client.submit(ENDPOINT, arguments=arguments)

    for status in controller.poll_request_status():
        print(f"[{controller.request_id}] {status.__class__.__name__}")

    return controller.get()


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: generate_video.py <prompt>", file=sys.stderr)
        return 2

    prompt = sys.argv[1]

    try:
        result = generate_video(prompt)
    except CredentialsMissedError as exc:
        print(f"credentials error: {exc}", file=sys.stderr)
        return 1
    except HiggsfieldClientError as exc:
        print(f"request failed: {exc}", file=sys.stderr)
        return 1

    video_url = result.get("video", {}).get("url")
    if not video_url:
        print(f"unexpected response: {result}", file=sys.stderr)
        return 1

    print(video_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
