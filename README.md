# VoiceList (Android)

VoiceList is a simple Android grocery list app that lets you speak items into your list, ask what is on the list, and clear it when you are done.

## What it does
- **Add item**: Tap “Add item” and say the grocery item. It is saved to your list.
- **Read list**: Tap “Read list” and say “what’s on my list.” The app reads your list back.
- **Clear list**: Tap “Clear list” to reset everything.

## How to run
1. Open the project in Android Studio.
2. Let Gradle sync.
3. Run the `app` configuration on an emulator or device.
4. Accept the microphone permission when prompted.

## Notes
- Android’s built-in speech recognition is used, so a network connection may be required depending on the device.
- If you want hotword activation ("Hey VoiceList"), you can integrate a hotword SDK later.
