from django.dispatch import receiver

@receiver(signals.post_init)
def my_function(sender, **kwargs):
    print("hi")
