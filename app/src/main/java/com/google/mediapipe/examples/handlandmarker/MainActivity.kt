package com.google.mediapipe.examples.handlandmarker

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.os.Build
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.viewModels
import androidx.annotation.RequiresPermission
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.setupWithNavController
import java.io.OutputStream
import java.util.UUID
import com.google.mediapipe.examples.handlandmarker.R

class MainActivity : AppCompatActivity() {

    lateinit var gestureTextView: TextView
    private lateinit var connectButton: Button

    private val viewModel: MainViewModel by viewModels()

    private var btSocket: BluetoothSocket? = null
    private var btOut: OutputStream? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        gestureTextView = findViewById(R.id.gestureTextView)
        connectButton = findViewById(R.id.btnConnectBluetooth)

        val navHostFragment =
            supportFragmentManager.findFragmentById(R.id.fragment_container) as NavHostFragment
        val navController = navHostFragment.navController
        val bottomNav = findViewById<com.google.android.material.bottomnavigation.BottomNavigationView>(
            R.id.navigation
        )
        bottomNav.setupWithNavController(navController)
        bottomNav.setOnNavigationItemReselectedListener { /* ignore reselection */ }

        connectButton.setOnClickListener {
            showBluetoothDeviceDialog()
        }

        requestBtPermissionsIfNeeded()
    }

    // CameraFragment will call this
    fun sendFingerStates(states: List<Int>) {
        val out = btOut ?: return
        val data = states.map { it.toByte() }.toByteArray()
        try {
            out.write(data)
        } catch (e: Exception) {
            runOnUiThread {
                Toast.makeText(this, "BT write error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun showBluetoothDeviceDialog() {
        val adapter = BluetoothAdapter.getDefaultAdapter()
        if (adapter == null || !adapter.isEnabled) {
            Toast.makeText(this, "Bluetooth disabled", Toast.LENGTH_SHORT).show()
            return
        }

        // Check permission for Android 12+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (checkSelfPermission(android.Manifest.permission.BLUETOOTH_CONNECT) !=
                android.content.pm.PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Bluetooth permission not granted", Toast.LENGTH_SHORT).show()
                return
            }
        }

        // Get bonded devices
        val devices = adapter.bondedDevices?.toList() ?: emptyList()

        if (devices.isEmpty()) {
            Toast.makeText(this, "No paired devices", Toast.LENGTH_SHORT).show()
            return
        }

        val names = devices.map { "${it.name ?: "Unknown"} (${it.address})" }.toTypedArray()

        AlertDialog.Builder(this)
            .setTitle("Select Bluetooth device")
            .setItems(names) { _, which ->
                val device = devices[which]
                connectToDevice(device)
            }
            .show()
    }

    private fun connectToDevice(device: BluetoothDevice) {
        Thread @androidx.annotation.RequiresPermission(android.Manifest.permission.BLUETOOTH_CONNECT) {
            try {
                val uuid =
                    UUID.fromString("00001101-0000-1000-8000-00805F9B34FB") // SPP UUID
                val socket = device.createRfcommSocketToServiceRecord(uuid)
                socket.connect()
                btSocket = socket
                btOut = socket.outputStream
                runOnUiThread @RequiresPermission(Manifest.permission.BLUETOOTH_CONNECT) {
                    Toast.makeText(
                        this,
                        "Connected to ${device.name ?: "device"}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(
                        this,
                        "BT connect failed: ${e.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }.start()
    }

    private fun requestBtPermissionsIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val perms = mutableListOf<String>()
            perms.add(android.Manifest.permission.BLUETOOTH_CONNECT)
            perms.add(android.Manifest.permission.BLUETOOTH_SCAN)
            requestPermissions(perms.toTypedArray(), 1001)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            btOut?.close()
            btSocket?.close()
        } catch (_: Exception) {
        }
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        super.onBackPressed()
        finish()
    }
}
