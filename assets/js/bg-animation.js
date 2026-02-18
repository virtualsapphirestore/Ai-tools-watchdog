document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('bg-animation-container');
    if (!container) return;

    const frameCount = 60;
    const basePath = 'assets/images/bg-sequence/grok-video-433ac25d-d317-4660-bcd2-f2d148fc3655_';
    const images = [];
    const fps = 24; 
    const interval = 1000 / fps;
    
    let currentFrame = 0;
    let lastTime = 0;

    // Helper to load image
    const loadImage = (index) => {
        const img = new Image();
        const num = index.toString().padStart(3, '0');
        img.src = `${basePath}${num}.jpg`;
        return img;
    };

    // Preload all images
    for (let i = 0; i < frameCount; i++) {
        images.push(loadImage(i));
    }

    function animate(timestamp) {
        if (!lastTime) lastTime = timestamp;
        const elapsed = timestamp - lastTime;

        if (elapsed > interval) {
            const img = images[currentFrame];
            // Only update if image is loaded, otherwise skip or wait? 
            // Better to display what we have to keep rhythm, or just check complete.
            if (img && img.complete && img.naturalHeight !== 0) {
                 container.style.backgroundImage = `url("${img.src}")`;
            }
            
            currentFrame = (currentFrame + 1) % frameCount;
            lastTime = timestamp - (elapsed % interval); // Adjust for drift
        }

        requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
});
