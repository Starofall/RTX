package crowdnav

import com.github.benfradet.spark.kafka.writer.KafkaWriter._
import kafka.serializer.StringDecoder
import org.apache.kafka.clients.producer.ProducerRecord
import org.apache.kafka.common.serialization.StringSerializer
import org.apache.spark._
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.json4s.DefaultFormats
import org.json4s.jackson.Serialization.{read, write}
import scala.util.Random
import java.util.Properties

object Main extends App {

  // the kafka uri
  val kafkaURI = "kafka:9092"
  // the zookeeper uri
  val zookeeperURI = "kafka:2181"
  // the queue we get our input from
  val kafkaInputQueue = "crowd-nav-trips"
  // the queue we add our results to
  val kafkaOutputQueue = "crowd-nav-summary"

  // create a new spark config
  val sparkConf = new SparkConf().setAppName("CrowdNavSpark")
  // create a streaming context with a 1 seconds window
  val ssc = new StreamingContext(sparkConf, Seconds(1))
  // definition of the kafka consumer
  val kafkaConf = Map(
    "metadata.broker.list" -> kafkaURI,
    "zookeeper.connect" -> zookeeperURI,
    "group.id" -> Random.nextLong().toString, // not ideal, but we want a new random groupid every time
    "zookeeper.connection.timeout.ms" -> "1000")
  // create a kafka stream using spark streaming
  val kafkaStream = KafkaUtils.createStream[String, String, StringDecoder, StringDecoder](ssc,
    kafkaConf, Map(kafkaInputQueue -> 1), StorageLevel.MEMORY_ONLY)
  // config for kafka producer
  val producerConfig = {
    val p = new Properties()
    p.setProperty("bootstrap.servers", kafkaURI)
    p.setProperty("key.serializer", classOf[StringSerializer].getName)
    p.setProperty("value.serializer", classOf[StringSerializer].getName)
    p
  }
  // format used for json serialization
  implicit val formats = DefaultFormats
  // parses the kafka stream into EfficiencyInput case classes
  val jsonParsed = kafkaStream.map(m => read[OverheadInput](m._2))
  // set the count to 1 for default
  val countSet = jsonParsed.map(_.copy(count = Some(1)))
  // reduces the list into a single EfficiencyInput
  val processed = countSet.reduce((input: OverheadInput, input0: OverheadInput) =>
    OverheadInput(input.overhead + input0.overhead, 0,
      Some(input.count.getOrElse(1) + input0.count.getOrElse(1)))
  )
  // write the results back to a kafka queue
  processed.writeToKafka(producerConfig, s => new ProducerRecord[String, String](kafkaOutputQueue, write(s)))
  // start streaming
  ssc.start()
  // do forever
  ssc.awaitTermination()
}

// a wrapper object for our input messages
case class OverheadInput(overhead: Double, tick: Int, count: Option[Int])