/**
 * AI 電商行銷設計師 Ultra - Interactive Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Reveal Animations on Scroll
    const reveals = document.querySelectorAll('.reveal, .grid-item');
    
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        reveals.forEach(el => {
            const revealTop = el.getBoundingClientRect().top;
            const revealPoint = 100;
            
            if (revealTop < windowHeight - revealPoint) {
                el.classList.add('active');
                if (el.classList.contains('grid-item')) {
                    el.classList.add('visible');
                }
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Trigger once on load

    // 2. Category Filtering Logic
    const filterButtons = document.querySelectorAll('.filter-btn');
    const gridItems = document.querySelectorAll('.grid-item');
    const masonryGrid = document.getElementById('masonry-grid');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            gridItems.forEach(item => {
                const category = item.getAttribute('data-category');
                
                // Hide or show based on filter
                if (filterValue === 'all' || category === filterValue) {
                    item.classList.remove('filtered-out');
                    // Small delay for fade in animation
                    setTimeout(() => {
                        item.classList.add('visible');
                    }, 50);
                } else {
                    item.classList.add('filtered-out');
                    item.classList.remove('visible');
                }
            });

            // Re-trigger reveal check
            revealOnScroll();
        });
    });

    // 3. Lightbox Logic
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const closeLightbox = document.querySelector('.close-lightbox');

    gridItems.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            lightboxImg.src = img.src;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden'; // Disable scroll
        });
    });

    const closeLightboxHandler = () => {
        lightbox.classList.remove('active');
        document.body.style.overflow = ''; // Enable scroll
    };

    closeLightbox.addEventListener('click', closeLightboxHandler);
    
    // Close on click outside image
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightboxHandler();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightboxHandler();
        }
    });
});
