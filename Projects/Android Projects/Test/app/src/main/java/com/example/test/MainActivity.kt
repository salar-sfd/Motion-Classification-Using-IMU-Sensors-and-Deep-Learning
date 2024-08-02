import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import java.io.IOException
import java.util.*

class BluetoothSender : AppCompatActivity() {

    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var device: BluetoothDevice
    private lateinit var socket: BluetoothSocket

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Set up Bluetooth adapter
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()
        if (bluetoothAdapter == null) {
            Log.e(TAG, "Device doesn't support Bluetooth")
            return
        }

        // Set up desired Bluetooth device
        val deviceAddress = "00:00:00:00:00:00" // Replace with the desired device's MAC address
        device = bluetoothAdapter.getRemoteDevice(deviceAddress)

        // Connect to the Bluetooth device
        connectToDevice()
    }

    private fun connectToDevice() {
        val uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB") // Standard SPP UUID
        try {
            socket = device.createRfcommSocketToServiceRecord(uuid)
            socket.connect()
            Log.i(TAG, "Connected to device: ${device.name}")
            sendDataForever()
        } catch (e: IOException) {
            Log.e(TAG, "Error connecting to device: ${device.name}", e)
        }
    }

    private fun sendDataForever() {
        val outputStream = socket.outputStream
        val data = "s"
        while (true) {
            try {
                outputStream.write(data.toByteArray())
                Thread.sleep(1000) // Adjust the delay between each send as needed
            } catch (e: IOException) {
                Log.e(TAG, "Error sending data to device: ${device.name}", e)
                break
            } catch (e: InterruptedException) {
                Log.e(TAG, "Thread interrupted", e)
                break
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            socket.close()
        } catch (e: IOException) {
            Log.e(TAG, "Error closing socket", e)
        }
    }

    companion object {
        private const val TAG = "BluetoothSender"
    }
}