
document.addEventListener('DOMContentLoaded', function () {
    // Check if we've shown the intro in this session
    if (sessionStorage.getItem('introShown')) {
        return;
    }

    const overlay = document.getElementById('intro-overlay');
    if (!overlay) return;

    overlay.style.display = 'flex';
    const canvas = document.getElementById('intro-canvas');
    const ctx = canvas.getContext('2d');

    let width, height;
    let particles = [];

    // Configuration
    const text = "Made by Priyansh";
    const particleSize = 2; // Smaller particles for better resolution
    const particleColor = '#ffffff'; // White text
    const mouseRadius = 100;
    const animationDuration = 4000; // Total time before fade out

    function init() {
        resize();
        window.addEventListener('resize', resize);

        // Create particles from text
        createParticlesFromText();

        // Start animation loop
        animate();

        // Fade out after duration
        setTimeout(() => {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.style.display = 'none';
                sessionStorage.setItem('introShown', 'true');
                // Stop animation to save resources
                cancelAnimationFrame(animationId);
            }, 1000);
        }, animationDuration);
    }

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    function createParticlesFromText() {
        particles = [];

        ctx.fillStyle = 'white';
        ctx.font = 'bold 80px sans-serif'; // Adjust size as needed
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // Draw text to canvas temporarily to get pixel data
        ctx.fillText(text, width / 2, height / 2);

        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;

        ctx.clearRect(0, 0, width, height); // Clear the text

        // Sample pixels to create particles
        for (let y = 0; y < height; y += 4) { // Step size determines density
            for (let x = 0; x < width; x += 4) {
                const index = (y * width + x) * 4;
                const alpha = data[index + 3];

                if (alpha > 128) {
                    // This pixel is part of the text
                    particles.push(new Particle(x, y));
                }
            }
        }
    }

    class Particle {
        constructor(x, y) {
            this.x = Math.random() * width; // Start at random position
            this.y = Math.random() * height;
            this.targetX = x;
            this.targetY = y;
            this.vx = (Math.random() - 0.5) * 2;
            this.vy = (Math.random() - 0.5) * 2;
            this.size = Math.random() * particleSize + 1;
            this.color = particleColor;

            // Random start delay for "assembling" effect
            this.delay = Math.random() * 50;
            this.timer = 0;
        }

        update() {
            this.timer++;

            if (this.timer < this.delay) return;

            // Move towards target
            const dx = this.targetX - this.x;
            const dy = this.targetY - this.y;

            this.x += dx * 0.05; // Ease factor
            this.y += dy * 0.05;

            // Add some jitter for 3D-ish noise effect
            // this.x += (Math.random() - 0.5) * 0.5;
            // this.y += (Math.random() - 0.5) * 0.5;
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    let animationId;
    function animate() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'; // Trail effect
        ctx.fillRect(0, 0, width, height);

        particles.forEach(p => {
            p.update();
            p.draw();
        });

        // Connect particles for "mesh" look (optional, expensive for many particles)
        // connectParticles();

        animationId = requestAnimationFrame(animate);
    }

    init();
});
