/**
 * Ultra - Pinterest Style Dynamic Grid
 */

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('masonry-grid');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxCategory = document.getElementById('lightbox-category');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('search-input');
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');
    const menuIcon = menuToggle.querySelector('.material-symbols-outlined');

    let allWorks = [];

    // 1. Fetch Works Data
    fetch('data/works.json')
        .then(response => response.json())
        .then(data => {
            // Sort by Date Descending (Newest First)
            allWorks = data.sort((a, b) => new Date(b.date) - new Date(a.date));
            renderGrid(allWorks);
        })
        .catch(err => {
            console.error('Error loading works:', err);
            grid.innerHTML = '<p class="error">暫時無法載入作品，請稍後再試。</p>';
        });

    // 2. Render Grid Function
    function renderGrid(works) {
        grid.innerHTML = '';
        if (works.length === 0) {
            grid.innerHTML = '<p class="no-results">找不到相關作品。</p>';
            return;
        }

        works.forEach((item, index) => {
            const gridItem = document.createElement('div');
            gridItem.className = 'grid-item';
            gridItem.dataset.category = item.category;
            gridItem.style.animationDelay = `${index * 0.05}s`;

            gridItem.innerHTML = `
                <img src="${item.image}" alt="${item.title}" loading="lazy">
                <div class="item-overlay">
                    <button class="save-btn">儲存</button>
                    <div class="item-meta">
                         <span class="item-title-hover">${item.title}</span>
                         <span class="item-date">${item.date}</span>
                    </div>
                </div>
            `;

            gridItem.addEventListener('click', () => openLightbox(item));
            grid.appendChild(gridItem);
        });
    }

    // 3. Lightbox Logic
    function openLightbox(item) {
        lightboxImg.src = item.image;
        lightboxTitle.textContent = item.title;
        lightboxCategory.textContent = translateCategory(item.category) + ' • ' + item.date;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function translateCategory(cat) {
        const mapping = {
            'ad-creatives': '廣告素材',
            'marketing-visuals': '行銷視覺',
            'landing-pages': '網頁設計',
            'branding': '品牌概念',
            'social-media': '社群行銷'
        };
        return mapping[cat] || cat;
    }

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.classList.contains('active')) {
            lightbox.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });

    // 4. Filtering Logic
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            
            // UI Toggle
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Data Filter
            const filtered = filter === 'all' 
                ? allWorks 
                : allWorks.filter(w => w.category === filter);
            
            renderGrid(filtered);
        });
    });

    // 5. Search Logic (Optional - only if input exists)
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const filtered = allWorks.filter(w => 
                w.title.toLowerCase().includes(query) || 
                translateCategory(w.category).includes(query) ||
                w.date.includes(query)
            );
            renderGrid(filtered);
        });
    }

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (lightbox.classList.contains('active')) {
                lightbox.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
            if (navLinks.classList.contains('active')) {
                toggleMenu();
            }
        }
    });

    // Mobile Menu Toggle Logic
    function toggleMenu() {
        navLinks.classList.toggle('active');
        const isActive = navLinks.classList.contains('active');
        menuIcon.textContent = isActive ? 'close' : 'menu';
        document.body.style.overflow = isActive ? 'hidden' : 'auto';
    }

    menuToggle.addEventListener('click', toggleMenu);

    // Close menu when clicking on a link (mobile)
    navLinks.querySelectorAll('.nav-link, .cta-button').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('active')) {
                toggleMenu();
            }
        });
    });
});
