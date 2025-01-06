// assets/js/secretToggles.js

export function initSecretToggles() {
    // Instead of numeric keyCodes, we now match e.key strings
    // Updated Konami sequence: 
    // ArrowUp, ArrowUp, ArrowDown, ArrowDown, ArrowLeft, ArrowRight, ArrowLeft, ArrowRight, b, a
    const konamiSequence = [
        'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
        'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
        'b', 'a'
    ];
    let konamiIndex = 0;

    // Listen for keydown for Konami code
    document.addEventListener('keydown', (e) => {
        // If user presses the correct key in the sequence...
        if (e.key === konamiSequence[konamiIndex]) {
            konamiIndex++;
            // If all keys in the sequence have been pressed...
            if (konamiIndex === konamiSequence.length) {
                const secretCodeDiv = document.getElementById('secret-code');
                if (secretCodeDiv) {
                    secretCodeDiv.style.display = 'block';
                }
                alert('You unlocked the secret mode!');
                konamiIndex = 0; // reset
            }
        } else {
            // If wrong key, reset to 0
            konamiIndex = 0;
        }
    });

    // Another secret code: "opensesame"
    // We'll use e.key here as well, converting to lowercase
    let typedInput = '';
    const secretPhrase = 'opensesame';

    document.addEventListener('keypress', (e) => {
        typedInput += e.key.toLowerCase();
        if (typedInput.includes(secretPhrase)) {
            const secretDiv = document.getElementById('secret-code');
            if (secretDiv) {
                secretDiv.style.display = 'block';
                alert('🔓 Secret content unlocked!');
            }
            typedInput = ''; // reset
        }
        // If typedInput grows too large, trim it
        if (typedInput.length > secretPhrase.length) {
            typedInput = typedInput.substr(typedInput.length - secretPhrase.length);
        }
    });
}
