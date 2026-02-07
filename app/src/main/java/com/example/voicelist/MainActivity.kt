package com.example.voicelist

import android.Manifest
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.ListView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import java.util.Locale

class MainActivity : AppCompatActivity(), TextToSpeech.OnInitListener {
    private lateinit var listView: ListView
    private lateinit var addButton: Button
    private lateinit var readButton: Button
    private lateinit var clearButton: Button
    private lateinit var adapter: ArrayAdapter<String>
    private lateinit var prefs: SharedPreferences
    private lateinit var textToSpeech: TextToSpeech
    private val items = mutableListOf<String>()

    private val requestAudioPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (!granted) {
            Toast.makeText(this, "Microphone permission is required for voice input", Toast.LENGTH_LONG).show()
        }
    }

    private val addItemRecognizer = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        val data = result.data
        val matches = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
        val text = matches?.firstOrNull()?.trim().orEmpty()
        if (text.isNotEmpty()) {
            items.add(text)
            adapter.notifyDataSetChanged()
            saveItems()
            speak("Added $text")
        } else {
            Toast.makeText(this, "No item heard", Toast.LENGTH_SHORT).show()
        }
    }

    private val readListRecognizer = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        val data = result.data
        val matches = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
        val text = matches?.firstOrNull()?.trim().orEmpty()
        if (text.contains("list", ignoreCase = true)) {
            readList()
        } else {
            Toast.makeText(this, "Say 'what's on my list'", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        prefs = getSharedPreferences("voice_list", MODE_PRIVATE)
        textToSpeech = TextToSpeech(this, this)

        listView = findViewById(R.id.listView)
        addButton = findViewById(R.id.addButton)
        readButton = findViewById(R.id.readButton)
        clearButton = findViewById(R.id.clearButton)

        items.addAll(loadItems())
        adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, items)
        listView.adapter = adapter

        addButton.setOnClickListener {
            startVoiceInput(
                prompt = getString(R.string.speech_prompt_add),
                launcher = addItemRecognizer
            )
        }

        readButton.setOnClickListener {
            startVoiceInput(
                prompt = getString(R.string.speech_prompt_read),
                launcher = readListRecognizer
            )
        }

        clearButton.setOnClickListener {
            items.clear()
            adapter.notifyDataSetChanged()
            saveItems()
            speak("List cleared")
        }

        ensureAudioPermission()
    }

    override fun onDestroy() {
        textToSpeech.stop()
        textToSpeech.shutdown()
        super.onDestroy()
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            textToSpeech.language = Locale.US
        }
    }

    private fun startVoiceInput(
        prompt: String,
        launcher: androidx.activity.result.ActivityResultLauncher<Intent>
    ) {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            Toast.makeText(this, "Speech recognition not available", Toast.LENGTH_LONG).show()
            return
        }
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
            putExtra(RecognizerIntent.EXTRA_PROMPT, prompt)
        }
        launcher.launch(intent)
    }

    private fun readList() {
        val message = if (items.isEmpty()) {
            getString(R.string.empty_list)
        } else {
            "You have ${items.joinToString(", ")}".
        }
        speak(message)
    }

    private fun speak(message: String) {
        textToSpeech.speak(message, TextToSpeech.QUEUE_FLUSH, null, "voice_list")
    }

    private fun loadItems(): List<String> {
        val stored = prefs.getString("items", "").orEmpty()
        if (stored.isBlank()) return emptyList()
        return stored.split("\n").filter { it.isNotBlank() }
    }

    private fun saveItems() {
        prefs.edit().putString("items", items.joinToString("\n")).apply()
    }

    private fun ensureAudioPermission() {
        val granted = ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED
        if (!granted) {
            requestAudioPermission.launch(Manifest.permission.RECORD_AUDIO)
        }
    }
}
