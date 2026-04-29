plugins {
    id("com.android.application")
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "net.nativemind.bhagavadgita.book.bhagavadgita_book"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "net.nativemind.bhagavadgita.book.bhagavadgita_book"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        create("release") {
            val keystorePath = System.getenv("ANDROID_KEYSTORE_PATH")
            val keystorePassword = System.getenv("ANDROID_KEYSTORE_PASSWORD")
            val keyAlias = System.getenv("ANDROID_KEY_ALIAS")
            val keyPassword = System.getenv("ANDROID_KEY_PASSWORD")

            if (!keystorePath.isNullOrBlank()
                && !keystorePassword.isNullOrBlank()
                && !keyAlias.isNullOrBlank()
                && !keyPassword.isNullOrBlank()
            ) {
                storeFile = file(keystorePath)
                storePassword = keystorePassword
                this.keyAlias = keyAlias
                this.keyPassword = keyPassword
            }
        }
    }

    buildTypes {
        release {
            val hasReleaseSigning =
                !System.getenv("ANDROID_KEYSTORE_PATH").isNullOrBlank() &&
                    !System.getenv("ANDROID_KEYSTORE_PASSWORD").isNullOrBlank() &&
                    !System.getenv("ANDROID_KEY_ALIAS").isNullOrBlank() &&
                    !System.getenv("ANDROID_KEY_PASSWORD").isNullOrBlank()

            signingConfig = if (hasReleaseSigning) {
                signingConfigs.getByName("release")
            } else {
                // Keeps local/dev builds working; CI can provide release signing via env vars.
                signingConfigs.getByName("debug")
            }
        }
    }
}

flutter {
    source = "../.."
}
