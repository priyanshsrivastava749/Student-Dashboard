document.addEventListener('DOMContentLoaded', function () {
    // Check for success messages to play audio
    const messages = document.querySelectorAll('.message-tag');
    messages.forEach(msg => {
        if (msg.dataset.tag === 'success' && msg.innerText.includes('Homework submitted')) {
            const audio = new Audio('/static/audio/1.mp3');
            audio.play().catch(e => console.log("Audio play failed (interaction needed):", e));
        }
    });

    // Modal/Toggle logic
    const submitBtn = document.getElementById('btn-submit-hw');
    const doubtBtn = document.getElementById('btn-ask-doubt');
    const submitSection = document.getElementById('section-submit-hw');
    const doubtSection = document.getElementById('section-ask-doubt');

    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            submitSection.style.display = submitSection.style.display === 'none' ? 'block' : 'none';
            doubtSection.style.display = 'none';
        });
    }

    if (doubtBtn) {
        doubtBtn.addEventListener('click', () => {
            doubtSection.style.display = doubtSection.style.display === 'none' ? 'block' : 'none';
            submitSection.style.display = 'none';
        });
    }
});
