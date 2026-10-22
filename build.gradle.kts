import com.android.build.gradle.BaseExtension
import com.lagradost.cloudstream3.gradle.CloudstreamExtension
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.tasks.KotlinJvmCompile

buildscript {
    repositories {
        google()
        mavenCentral()
        // Shitpack repo which contains our tools and dependencies
        maven("https://jitpack.io")
    }

    dependencies {
        classpath("com.android.tools.build:gradle:8.7.3")
        // Cloudstream gradle plugin which makes everything work and builds plugins
        classpath("com.github.recloudstream:gradle:-SNAPSHOT")
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:2.4.0") // matches current cloudstream stub metadata (2.4.0)
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
}

fun Project.cloudstream(configuration: CloudstreamExtension.() -> Unit) = extensions.getByName<CloudstreamExtension>("cloudstream").configuration()

fun Project.android(configuration: BaseExtension.() -> Unit) = extensions.getByName<BaseExtension>("android").configuration()

subprojects {
    apply(plugin = "com.android.library")
    apply(plugin = "kotlin-android")
    apply(plugin = "com.lagradost.cloudstream3.gradle")

    cloudstream {
        // when running through github workflow, GITHUB_REPOSITORY should contain current repository name
        setRepo(System.getenv("GITHUB_REPOSITORY") ?: "user/repo")
    }

    android {
        namespace = "com.example"

        defaultConfig {
            minSdk = 21
            compileSdkVersion(35)
            targetSdk = 35
        }

        compileOptions {
            sourceCompatibility = JavaVersion.VERSION_11
            targetCompatibility = JavaVersion.VERSION_11
        }

        tasks.withType<KotlinJvmCompile> {
            compilerOptions {
                jvmTarget.set(JvmTarget.JVM_11) // current cloudstream stub is JVM-11 bytecode; inlining requires >= 11
                freeCompilerArgs.addAll(
                    "-Xno-call-assertions",
                    "-Xno-param-assertions",
                    "-Xno-receiver-assertions"
                )
            }
        }
    }

    dependencies {
        val cloudstream by configurations
        val implementation by configurations

        // Stubs for all cloudstream classes
        cloudstream("com.lagradost:cloudstream3:pre-release")

        // These dependencies can include any of those which are added by the app,
        // but you don't need to include any of them if you don't need them.
        // https://github.com/recloudstream/cloudstream/blob/master/app/build.gradle.kts
        implementation(kotlin("stdlib")) // Adds Standard Kotlin Features
        implementation("com.github.Blatzar:NiceHttp:0.4.13") // HTTP Lib (matches bob-source)
        implementation("org.jsoup:jsoup:1.19.1") // HTML Parser (matches bob-source)
        implementation("org.jspecify:jspecify:1.0.0") // annotation-only; jsoup 1.19 API references org.jspecify @Nullable
        // IMPORTANT: Do not bump Jackson above 2.13.1, as newer versions will
        // break compatibility on older Android devices.
        implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.13.1") // JSON Parser
        implementation("com.fasterxml.jackson.core:jackson-databind:2.16.0") // JSON-nesne dönüştürme (matches bob-source)
        implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.1") // asenkron işlemler (matches bob-source)
        implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.8.0") // (matches bob-source)
    }
}

task<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}