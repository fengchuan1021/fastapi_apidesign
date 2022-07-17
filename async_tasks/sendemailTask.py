from celery_app import celery_app
@celery_app.task(name='sendconfirmemailtouser')
def sayHello(name):
    print(name)
    print('helloworld')