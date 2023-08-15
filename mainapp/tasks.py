from celery import shared_task

@shared_task(bind=True)
def test_functions(self, args):
    print(args)
    # for i in range(int(args[0])):
    #     print(i)
    return "DONE"
