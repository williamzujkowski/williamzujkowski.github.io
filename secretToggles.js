// secretToggles.js

export function initSecretToggles() {
    // Konami Code
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    let index = 0;
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === konamiCode[index]) {
            index++;
            if (index === konamiCode.length) {
                const secretCodeDiv = document.getElementById('secret-code');
                if (secretCodeDiv) {
                    secretCodeDiv.style.display = 'block';
                }
                alert('You unlocked the secret mode!');
                index = 0;
            }
        } else {
            index = 0;
        }
    });

    // Another secret code: "opensesame"
    let input = '';
    const secretPhrase = 'opensesame';
    document.addEventListener('keypress', function (e) {
        input += e.key.toLowerCase();
        if (input.includes(secretPhrase)) {
            const sc = document.getElementById('secret-code');
            if (sc) {
                sc.style.display = 'block';
                alert('🔓 Secret content unlocked!');
            }
            input = '';
        }
        if (input.length > secretPhrase.length) {
            input = input.substr(input.length - secretPhrase.length);
        }
    });
}
