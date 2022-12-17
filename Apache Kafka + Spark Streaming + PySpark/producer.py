from kafka import KafkaProducer

producer=KafkaProducer(bootstrap_servers='localhost:9092')

producer.send('input_recommend_product',b'(1,Main Menu),(2,Phone),(3,Smart Phone),(4,iPhone)')

producer.close()

