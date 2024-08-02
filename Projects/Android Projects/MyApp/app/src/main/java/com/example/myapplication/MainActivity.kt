package com.example.myapplication

import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication.ui.theme.MyApplicationTheme

class MainActivity : ComponentActivity(), SensorEventListener {
    private lateinit var sensorManager: SensorManager
    private val accelerometerValues = mutableStateListOf<Float?>(null, null, null)
    private val gyroscopeValues = mutableStateListOf<Float?>(null, null, null)
    private val compassValues = mutableStateListOf<Float?>(null)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
                val accelerometerSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
                val gyroscopeSensor = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
                val compassSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION)
                sensorManager.registerListener(this@MainActivity, accelerometerSensor, SensorManager.SENSOR_DELAY_NORMAL)
                sensorManager.registerListener(this@MainActivity, gyroscopeSensor, SensorManager.SENSOR_DELAY_NORMAL)
                sensorManager.registerListener(this@MainActivity, compassSensor, SensorManager.SENSOR_DELAY_NORMAL)

                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    Greeting("Android", accelerometerValues, gyroscopeValues, compassValues)
                }
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Not used in this example
    }

    override fun onSensorChanged(event: SensorEvent?) {
        when (event?.sensor?.type) {
            Sensor.TYPE_ACCELEROMETER -> {
                accelerometerValues[0] = event.values[0]
                accelerometerValues[1] = event.values[1]
                accelerometerValues[2] = event.values[2]
            }
            Sensor.TYPE_GYROSCOPE -> {
                gyroscopeValues[0] = event.values[0]
                gyroscopeValues[1] = event.values[1]
                gyroscopeValues[2] = event.values[2]
            }
            Sensor.TYPE_ORIENTATION -> {
                compassValues[0] = event.values[0]
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        sensorManager.unregisterListener(this)
    }
}

@Composable
fun Greeting(name: String, accelerometerValues: List<Float?>, gyroscopeValues: List<Float?>, compassValues: List<Float?>, modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Text(
            text = "Hello $name!",
            modifier = modifier
        )

        Text(
            text = "Accelerometer Values:",
            modifier = modifier
        )
        Text(
            text = "X: ${accelerometerValues[0] ?: "-"}",
            modifier = modifier
        )
        Text(
            text = "Y: ${accelerometerValues[1] ?: "-"}",
            modifier = modifier
        )
        Text(
            text = "Z: ${accelerometerValues[2] ?: "-"}",
            modifier = modifier
        )

        Text(
            text = "Gyroscope Values:",
            modifier = modifier
        )
        Text(
            text = "X: ${gyroscopeValues[0] ?: "-"}",
            modifier = modifier
        )
        Text(
            text = "Y: ${gyroscopeValues[1] ?: "-"}",
            modifier = modifier
        )
        Text(
            text = "Z: ${gyroscopeValues[2] ?: "-"}",
            modifier = modifier
        )

        Text(
            text = "Compass Values:",
            modifier = modifier
        )
        Text(
            text = "Heading: ${compassValues[0] ?: "-"}",
            modifier = modifier
        )
    }
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyApplicationTheme {
        Greeting("Android", listOf(1f, 2f, 3f), listOf(4f, 5f, 6f), listOf(180f))
    }
}
