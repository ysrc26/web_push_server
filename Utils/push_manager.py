from pywebpush import webpush, WebPushException


def send_web_push(subscription, data, private_key):
    result = None
    try:
        webpush(
            subscription_info=subscription,
            data=data,
            vapid_private_key=private_key,
            vapid_claims={"sub": "mailto:YourNameHere@example.org"}
        )
        result = "Push sent"
    except WebPushException as ex:
        result = "WebPush error! details: {0}".format(ex)
        if ex.response and ex.response.json():
            extra = ex.response.json()
            result = "Remote service replied with a {0}:{1}, {2}".format(extra.code, extra.errno, extra.message)

    return result
