lazy val root = (project in file(".")).
  settings(
    name := "CrowdNavSpark",
    version := "1.0",
    scalaVersion := "2.10.6",
    mainClass in Compile := Some("crowdnav.Main")
  )

assemblyOption in assembly ~= { _.copy(includeScala = false) }

libraryDependencies ++= Seq(
  "org.apache.spark" % "spark-core_2.10" % "1.6.3" % "provided",
  "org.apache.spark" % "spark-streaming_2.10" % "1.6.3" % "provided",
  "org.json4s" % "json4s-jackson_2.10" % "3.2.10",
  "com.github.benfradet" %% "spark-kafka-writer" % "0.1.0",
  ("org.apache.spark" % "spark-streaming-kafka_2.10" % "1.6.3").
    exclude("commons-beanutils", "commons-beanutils").
    exclude("commons-collections", "commons-collections").
    exclude("com.esotericsoftware.minlog", "minlog")
)

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs@_*)                 => MergeStrategy.discard
  case PathList("javax", "servlet", xs@_*)         => MergeStrategy.first
  case PathList(ps@_*) if ps.last endsWith ".html" => MergeStrategy.first
  case "application.conf"                          => MergeStrategy.concat
  case "unwanted.txt"                              => MergeStrategy.discard
  case x if x.startsWith("META-INF/ECLIPSEF.RSA")  => MergeStrategy.last
  case x if x.startsWith("META-INF/mailcap")       => MergeStrategy.last
  case x if x.startsWith("plugin.properties")      => MergeStrategy.last
  case x                                           => MergeStrategy.first
}
