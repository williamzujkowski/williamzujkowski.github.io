// assets/js/secretToggles.js

export function initSecretToggles() {
    // Konami Code with e.key
    const konamiSequence = [
        'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
        'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
        'b', 'a'
    ];
    let konamiIndex = 0;

    document.addEventListener('keydown', (e) => {
        if (e.key === konamiSequence[konamiIndex]) {
            konamiIndex++;
            if (konamiIndex === konamiSequence.length) {
                const secretCodeDiv = document.getElementById('secret-code');
                if (secretCodeDiv) {
                    secretCodeDiv.style.display = 'block';
                }
                alert('You unlocked the secret mode!');
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });

    // Another secret code: 'opensesame'
    let typedInput = '';
    const secretPhrase = 'opensesame';
    document.addEventListener('keypress', (e) => {
        typedInput += e.key.toLowerCase();
        if (typedInput.includes(secretPhrase)) {
            const sc = document.getElementById('secret-code');
            if (sc) {
                sc.style.display = 'block';
                alert('🔓 Secret content unlocked!');
            }
            typedInput = '';
        }
        if (typedInput.length > secretPhrase.length) {
            typedInput = typedInput.substr(typedInput.length - secretPhrase.length);
        }
    });
}
