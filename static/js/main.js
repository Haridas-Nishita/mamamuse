document.addEventListener('DOMContentLoaded', () => {
    // Handle flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });

    // Range input value display
    const moodRange = document.querySelector('input[type="range"]');
    if (moodRange) {
        const updateMoodValue = () => {
            const value = moodRange.value;
            const emoji = ['😢', '😕', '😐', '🙂', '😊', '😃', '🤗', '🥰', '😍', '🌟'][value - 1];
            moodRange.title = `Current mood: ${value}/10 ${emoji}`;
        };
        moodRange.addEventListener('input', updateMoodValue);
        updateMoodValue();
    }

    // Handle progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const progress = progressBar.getAttribute('data-progress');
        requestAnimationFrame(() => {
            progressBar.style.width = `${progress}%`;
        });
    }
});