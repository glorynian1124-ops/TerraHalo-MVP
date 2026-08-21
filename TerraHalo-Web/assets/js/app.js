/* =========================================================
   TerraHalo (沃土之环) 共享运行时
   导航注入 / 页脚 / Toast / 购物车 / 登录态 / 移动端抽屉
   ========================================================= */
(function (global) {
  'use strict';

  var LS_USER = 'th_user';
  var LS_CART = 'th_cart';

  /* ---------- 本地存储安全封装 ---------- */
  function read(key, fallback) {
    try {
      var v = localStorage.getItem(key);
      return v === null ? fallback : JSON.parse(v);
    } catch (e) { return fallback; }
  }
  function write(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) { /* ignore */ }
  }

  /* ---------- 工具 ---------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function fmtMoney(n) {
    return Number(n).toLocaleString('zh-CN', { maximumFractionDigits: 2 });
  }
  function refreshIcons(root) {
    if (global.lucide && typeof global.lucide.createIcons === 'function') {
      global.lucide.createIcons({ root: root || document });
    }
  }

  /* ---------- Toast ---------- */
  function toast(msg, type) {
    type = type || 'info';
    var wrap = document.querySelector('.th-toast-wrap');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.className = 'th-toast-wrap';
      document.body.appendChild(wrap);
    }
    var el = document.createElement('div');
    el.className = 'th-toast th-toast-' + type;
    var icoName = type === 'success' ? 'circle-check' : (type === 'error' ? 'circle-alert' : 'info');
    el.innerHTML = '<span class="th-toast-ico" data-lucide="' + icoName + '"></span><span>' + esc(msg) + '</span>';
    wrap.appendChild(el);
    refreshIcons(el);
    setTimeout(function () {
      el.classList.add('th-toast-out');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 260);
    }, 2200);
  }

  /* ---------- 购物车 ---------- */
  var Cart = {
    list: function () { return read(LS_CART, []); },
    _save: function (list) { write(LS_CART, list); },
    count: function () { return this.list().reduce(function (a, c) { return a + c.qty; }, 0); },
    total: function () { return this.list().reduce(function (a, c) { return a + c.qty * c.price; }, 0); },
    add: function (item) {
      var list = this.list();
      var found = list.find(function (c) { return c.id === item.id && c.spec === item.spec; });
      if (found) { found.qty += item.qty || 1; }
      else { list.push(Object.assign({}, item, { qty: item.qty || 1 })); }
      this._save(list);
      updateCartBadge();
    },
    setQty: function (id, spec, qty) {
      var list = this.list();
      var found = list.find(function (c) { return c.id === id && c.spec === spec; });
      if (found) {
        found.qty = qty;
        if (found.qty <= 0) list = list.filter(function (c) { return !(c.id === id && c.spec === spec); });
      }
      this._save(list);
      updateCartBadge();
    },
    remove: function (id, spec) {
      var list = this.list().filter(function (c) { return !(c.id === id && c.spec === spec); });
      this._save(list);
      updateCartBadge();
    },
    clear: function () {
      write(LS_CART, []);
      updateCartBadge();
    }
  };

  /* ---------- 原料采购车（厂商购买原料） ---------- */
  var MaterialCart = {
    LS: 'th_mat_cart',
    list: function () { return read(this.LS, []); },
    _save: function (list) { write(this.LS, list); },
    count: function () { return this.list().reduce(function (a, c) { return a + c.qty; }, 0); },
    totalWeight: function () { return this.list().reduce(function (a, c) { return a + c.qty; }, 0); },
    total: function () { return this.list().reduce(function (a, c) { return a + c.qty * c.price; }, 0); },
    add: function (item) {
      var list = this.list();
      var found = list.find(function (c) { return c.id === item.id; });
      if (found) { found.qty += item.qty || 1; }
      else { list.push(Object.assign({}, item, { qty: item.qty || 1 })); }
      this._save(list);
    },
    setQty: function (id, qty) {
      var list = this.list();
      var found = list.find(function (c) { return String(c.id) === String(id); });
      if (found) {
        found.qty = qty;
        if (found.qty <= 0) list = list.filter(function (c) { return String(c.id) !== String(id); });
      }
      this._save(list);
    },
    remove: function (id) {
      this._save(this.list().filter(function (c) { return String(c.id) !== String(id); }));
    },
    clear: function () { write(this.LS, []); }
  };

  /* ---------- 登录态 ---------- */
  var Auth = {
    current: function () { return read(LS_USER, null); },
    login: function (user) { write(LS_USER, user); },
    logout: function () {
      try { localStorage.removeItem(LS_USER); } catch (e) { /* ignore */ }
    }
  };

  /* ---------- 购物车角标 ---------- */
  function updateCartBadge() {
    var n = Cart.count();
    document.querySelectorAll('[data-cart-count]').forEach(function (b) {
      b.textContent = n;
      b.style.display = n > 0 ? 'flex' : 'none';
    });
  }

  /* ---------- 渲染购物车抽屉 ---------- */
  function renderCartPanel() {
    var list = Cart.list();
    var panel = document.getElementById('th-cart-panel');
    if (!panel) return;
    var total = Cart.total();
    if (!list.length) {
      panel.innerHTML = '<div class="th-body-sm" style="padding:32px 16px; text-align:center; color:var(--th-muted-foreground);">购物车还是空的</div>';
      return;
    }
    var rows = list.map(function (c) {
      return '<div class="th-cart-item" data-id="' + esc(c.id) + '" data-spec="' + esc(c.spec) + '">' +
        '<img src="' + esc(c.img) + '" alt="">' +
        '<div class="th-cart-item-info">' +
          '<div class="th-cart-item-name">' + esc(c.name) + '</div>' +
          '<div class="th-body-sm" style="color:var(--th-muted-foreground);">' + esc(c.spec) + '</div>' +
          '<div class="th-mono" style="color:var(--th-primary); font-weight:600;">¥' + fmtMoney(c.price) + '</div>' +
        '</div>' +
        '<div class="th-cart-qty">' +
          '<button type="button" class="th-cart-qty-btn" data-act="minus">−</button>' +
          '<span>' + c.qty + '</span>' +
          '<button type="button" class="th-cart-qty-btn" data-act="plus">+</button>' +
        '</div>' +
        '<button type="button" class="th-cart-remove" data-act="remove" aria-label="移除">×</button>' +
      '</div>';
    }).join('');
    panel.innerHTML = rows +
      '<div class="th-cart-foot">' +
        '<div class="th-cart-total"><span class="th-body-sm" style="color:var(--th-muted-foreground);">合计</span>' +
        '<span class="th-mono" style="font-size:1.25rem; font-weight:700; color:var(--th-primary);">¥' + fmtMoney(total) + '</span></div>' +
        '<button type="button" class="th-cart-checkout" id="th-cart-checkout">去结算</button>' +
      '</div>';
    refreshIcons(panel);
  }

  function toggleCart(open) {
    var panel = document.getElementById('th-cart-panel');
    if (!panel) return;
    if (typeof open === 'boolean') { panel.classList.toggle('open', open); }
    else { panel.classList.toggle('open'); }
    if (panel.classList.contains('open')) renderCartPanel();
  }

  function bindCartEvents() {
    document.addEventListener('click', function (e) {
      var panel = document.getElementById('th-cart-panel');
      if (panel && panel.classList.contains('open')) {
        var cartBtn = e.target.closest('[data-cart-toggle]');
        if (cartBtn) return; // 点击开关交给 toggle 处理
        if (!e.target.closest('#th-cart-panel')) toggleCart(false);
      }
    });
    document.addEventListener('click', function (e) {
      var item = e.target.closest('.th-cart-item');
      if (!item) return;
      var id = item.getAttribute('data-id');
      var spec = item.getAttribute('data-spec');
      var act = e.target.getAttribute('data-act') || (e.target.closest('[data-act]') ? e.target.closest('[data-act]').getAttribute('data-act') : '');
      var list = Cart.list();
      var cur = list.find(function (c) { return c.id === id && c.spec === spec; });
      if (!cur) return;
      if (act === 'plus') { Cart.setQty(id, spec, cur.qty + 1); }
      else if (act === 'minus') { Cart.setQty(id, spec, cur.qty - 1); }
      else if (act === 'remove') { Cart.remove(id, spec); }
      renderCartPanel();
    });
    document.addEventListener('click', function (e) {
      if (e.target && e.target.id === 'th-cart-checkout') {
        toast('结算功能为演示，购物车数据已保存在本地', 'info');
        toggleCart(false);
      }
    });
  }

  /* ---------- 导航渲染 ---------- */
  var NAVS = {
    public: [
      { label: '首页', href: 'index.html', key: 'home' },
      { label: '原料市场', href: 'materials.html', key: 'market' },
      { label: '有机肥商城', href: 'shop.html', key: 'shop' },
      { label: '企业情况', href: 'enterprises.html', key: 'enterprise' },
      { label: '司机调度', href: 'driver.html', key: 'driver' },
      { label: '关于我们', href: 'index.html#about', key: 'about' }
    ],
    driver: [
      { label: '首页', href: 'index.html', key: 'home' },
      { label: '任务中心', href: 'driver.html', key: 'tasks' },
      { label: '数据看板', href: 'driver.html', key: 'dashboard' },
      { label: '车辆管理', href: 'driver.html', key: 'vehicle' }
    ]
  };

  function renderNav(navType, activeKey) {
    var host = document.getElementById('th-nav');
    if (!host) return;
    var links = (NAVS[navType] || NAVS.public).slice();
    var user = Auth.current();
    var isAdmin = !!(user && user.role === 'admin');
    // 平台管理入口（企业情况 / 司机调度 / 管理后台）仅 admin 角色可见
    if (navType === 'public' && !isAdmin) {
      links = links.filter(function (l) {
        return l.key !== 'enterprise' && l.key !== 'driver' && l.key !== 'admin';
      });
    }
    if (navType === 'public' && isAdmin) {
      links.push({ label: '管理后台', href: 'admin.html', key: 'admin' });
    }

    var linkHtml = links.map(function (l) {
      var active = l.key === activeKey;
      var cls = 'th-body-sm no-underline transition-opacity hover:opacity-70' + (active ? ' font-semibold' : '');
      var color = active ? 'var(--th-primary)' : 'var(--th-foreground)';
      return '<a href="' + esc(l.href) + '" class="' + cls + '" style="color:' + color + ';">' + esc(l.label) + '</a>';
    }).join('');

    var drawerLinkHtml = links.map(function (l) {
      var active = l.key === activeKey;
      return '<a href="' + esc(l.href) + '" class="th-drawer-link' + (active ? ' th-drawer-link-active' : '') + '">' + esc(l.label) + '</a>';
    }).join('');

    var authHtml = '';
    if (user) {
      var initial = esc((user.name || '用').charAt(0));
      var roleHome = user.role === 'driver' ? 'driver.html' : (user.role === 'enterprise' ? 'enterprise.html' : 'index.html');
      authHtml = '<a href="' + roleHome + '" class="hidden md:flex items-center gap-2 no-underline" title="' + esc(user.name) + '">' +
        '<span class="inline-flex items-center justify-center w-8 h-8 rounded-full text-xs font-semibold" style="background:var(--th-primary); color:var(--th-primary-foreground);">' + initial + '</span>' +
        '<span class="th-body-sm" style="color:var(--th-foreground);">' + esc(user.name) + '</span></a>' +
        '<button id="th-logout" class="th-body-sm no-underline hidden md:inline-flex hover:opacity-70" style="background:none;border:none;cursor:pointer;color:var(--th-muted-foreground);padding:0;">退出</button>';
    } else {
      authHtml = '<a href="login.html" class="inline-flex items-center justify-center whitespace-nowrap rounded-full px-5 py-1.5 text-sm font-semibold no-underline transition-all hover:opacity-90 active:scale-[0.98]" style="background:var(--th-primary); color:var(--th-primary-foreground);">登录</a>';
    }

    var cartHtml = (navType === 'public') ? '<button data-cart-toggle class="relative inline-flex h-9 w-9 items-center justify-center rounded-full transition-colors hover:opacity-80" style="background:var(--th-secondary); color:var(--th-foreground);" aria-label="购物车">' +
      '<span data-lucide="shopping-cart" style="width:18px;height:18px;"></span>' +
      '<span data-cart-count class="absolute -top-0.5 -right-0.5 h-4 min-w-4 px-0.5 items-center justify-center rounded-full text-[10px] font-bold" style="background:var(--th-state-error); color:var(--th-background-50); display:none;">0</span></button>' : '';

    host.innerHTML =
      '<nav class="sticky top-0 z-50 w-full border-b" style="border-color:var(--th-border); background:color-mix(in srgb, var(--th-background) 80%, transparent); backdrop-filter:blur(16px) saturate(1.2); -webkit-backdrop-filter:blur(16px) saturate(1.2);">' +
        '<div class="mx-auto flex h-14 max-w-[1184px] items-center justify-between px-4 sm:px-6 lg:px-8">' +
          '<a href="index.html" class="flex items-center gap-2 no-underline" style="color:var(--th-foreground);">' +
            '<span class="text-xl leading-none" aria-hidden="true">🌱</span>' +
            '<span class="th-h3" style="font-size:1.125rem; color:var(--th-foreground);">沃土之环</span></a>' +
          '<div class="hidden md:flex items-center gap-6 th-nav-links">' + linkHtml + '</div>' +
          '<div class="flex items-center gap-2 sm:gap-3">' + cartHtml + authHtml +
            '<button data-nav-toggle class="md:hidden inline-flex items-center justify-center w-10 h-10" style="color:var(--th-foreground);background:transparent;border:none;cursor:pointer;border-radius:var(--th-radius-sm);" aria-label="菜单"><span data-lucide="menu" style="width:20px;height:20px;"></span></button>' +
          '</div>' +
        '</div>' +
      '</nav>' +
      '<div class="th-drawer" id="th-mobile-drawer"><div class="th-drawer-panel">' +
        '<div class="flex items-center justify-between mb-4">' +
          '<span class="th-h3" style="font-size:1.1rem;">导航</span>' +
          '<button data-nav-close class="inline-flex items-center justify-center w-9 h-9 rounded-full" style="background:var(--th-secondary);color:var(--th-foreground);border:none;cursor:pointer;"><span data-lucide="x" style="width:18px;height:18px;"></span></button>' +
        '</div>' + drawerLinkHtml +
        (user ? '<button id="th-logout-mobile" class="th-drawer-link" style="border:none;background:none;cursor:pointer;text-align:left;">退出登录</button>' : '<a href="login.html" class="th-drawer-link" style="color:var(--th-primary);font-weight:600;">登录 / 注册</a>') +
      '</div></div>';

    refreshIcons(host);
    updateCartBadge();
    bindNavEvents();
  }

  function bindNavEvents() {
    var drawer = document.getElementById('th-mobile-drawer');
    var openBtn = document.querySelector('[data-nav-toggle]');
    var closeBtn = document.querySelector('[data-nav-close]');
    if (openBtn && drawer) {
      openBtn.addEventListener('click', function () { drawer.classList.add('th-drawer-open'); });
    }
    if (closeBtn && drawer) {
      closeBtn.addEventListener('click', function () { drawer.classList.remove('th-drawer-open'); });
    }
    if (drawer) {
      drawer.addEventListener('click', function (e) { if (e.target === drawer) drawer.classList.remove('th-drawer-open'); });
    }
    var cartBtn = document.querySelector('[data-cart-toggle]');
    if (cartBtn) cartBtn.addEventListener('click', function (e) { e.stopPropagation(); toggleCart(); });
    var logoutBtn = document.getElementById('th-logout');
    var logoutMobile = document.getElementById('th-logout-mobile');
    function doLogout() { Auth.logout(); toast('已退出登录', 'info'); setTimeout(function () { location.reload(); }, 600); }
    if (logoutBtn) logoutBtn.addEventListener('click', doLogout);
    if (logoutMobile) logoutMobile.addEventListener('click', doLogout);
  }

  /* ---------- 页脚渲染 ---------- */
  function renderFooter(variant) {
    var host = document.getElementById('th-footer');
    if (!host) return;
    if (variant === 'light') {
      host.innerHTML = '<footer class="w-full border-t" style="border-color:var(--th-border); background:var(--th-muted);">' +
        '<div class="mx-auto max-w-[1184px] px-6 lg:px-8 py-8">' +
          '<div class="flex flex-col md:flex-row items-center justify-between gap-4">' +
            '<div class="flex items-center gap-2"><span class="text-lg" aria-hidden="true">🌱</span><span class="th-body-sm" style="color:var(--th-muted-foreground);">沃土之环 &copy; 2026</span></div>' +
            '<div class="flex items-center gap-6">' +
              '<a href="index.html#about" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-muted-foreground);">关于我们</a>' +
              '<a href="index.html#contact" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-muted-foreground);">联系方式</a>' +
              '<a href="login.html" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-muted-foreground);">隐私政策</a>' +
            '</div>' +
          '</div>' +
        '</div></footer>';
    } else {
      host.innerHTML = '<footer id="about" class="py-16 lg:py-20" style="background:var(--th-background-800);">' +
        '<div class="mx-auto max-w-[1184px] px-6 lg:px-8">' +
          '<div class="grid grid-cols-1 gap-10 md:grid-cols-3">' +
            '<div class="flex flex-col gap-3">' +
              '<div class="flex items-center gap-2"><span class="text-xl leading-none" aria-hidden="true">🌱</span><span class="th-h3" style="color:var(--th-text-100);">沃土之环</span></div>' +
              '<p class="th-body-sm" style="color:var(--th-text-300);">绿色农业 · 循环经济<br>连接农户、企业与司机的一站式平台</p>' +
            '</div>' +
            '<div class="flex flex-col gap-3">' +
              '<span class="text-sm font-semibold" style="color:var(--th-text-100);">快速链接</span>' +
              '<a href="materials.html" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-text-300);">原料市场</a>' +
              '<a href="shop.html" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-text-300);">有机肥商城</a>' +
              '<a href="driver.html" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-text-300);">司机收运</a>' +
              '<a href="index.html#about" class="th-body-sm no-underline transition-opacity hover:opacity-70" style="color:var(--th-text-300);">关于我们</a>' +
            '</div>' +
            '<div class="flex flex-col gap-3" id="contact">' +
              '<span class="text-sm font-semibold" style="color:var(--th-text-100);">联系我们</span>' +
              '<p class="th-body-sm" style="color:var(--th-text-300);">客服热线：400-888-9999</p>' +
              '<p class="th-body-sm" style="color:var(--th-text-300);">邮箱：contact@terrahalo.com</p>' +
              '<p class="th-body-sm" style="color:var(--th-text-300);">地址：北京市海淀区中关村科技园</p>' +
            '</div>' +
          '</div>' +
          '<div class="mt-12 border-t pt-8" style="border-color:var(--th-background-700);">' +
            '<p class="th-body-sm text-center" style="color:var(--th-text-400);">© 2026 沃土之环. 绿色农业 · 循环经济</p>' +
          '</div>' +
        '</div></footer>';
    }
  }

  /* ---------- 全局购物车抽屉挂载 ---------- */
  function mountCartShell() {
    if (document.getElementById('th-cart-panel')) return;
    var el = document.createElement('div');
    el.id = 'th-cart-panel';
    el.className = 'th-cart-panel';
    el.innerHTML = '<div class="th-cart-head"><span class="th-h3" style="font-size:1.05rem;">购物车</span>' +
      '<button type="button" id="th-cart-close" class="th-cart-close"><span data-lucide="x" style="width:16px;height:16px;"></span></button></div>' +
      '<div class="th-cart-body" id="th-cart-body"></div>';
    document.body.appendChild(el);
    var style = document.createElement('style');
    style.textContent = [
      '.th-cart-panel{position:fixed;top:64px;right:16px;z-index:95;width:min(360px,92vw);background:var(--th-card);border:1px solid var(--th-border);border-radius:var(--th-radius);box-shadow:var(--th-shadow-2xl);padding:16px;opacity:0;pointer-events:none;transform:translateY(-6px);transition:opacity .2s var(--th-ease),transform .2s var(--th-ease);}',
      '.th-cart-panel.open{opacity:1;pointer-events:auto;transform:translateY(0);}',
      '.th-cart-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;}',
      '.th-cart-close{background:var(--th-secondary);border:none;width:32px;height:32px;border-radius:var(--th-radius-full);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;color:var(--th-muted-foreground);}',
      '.th-cart-item{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--th-border);}',
      '.th-cart-item img{width:48px;height:48px;border-radius:var(--th-radius-sm);object-fit:cover;flex-shrink:0;}',
      '.th-cart-item-info{flex:1;min-width:0;}',
      '.th-cart-item-name{font-size:var(--th-font-size-sm);font-weight:600;color:var(--th-foreground);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}',
      '.th-cart-qty{display:flex;align-items:center;gap:8px;}',
      '.th-cart-qty-btn{width:26px;height:26px;border-radius:var(--th-radius-sm);border:1px solid var(--th-border);background:transparent;color:var(--th-foreground);cursor:pointer;line-height:1;}',
      '.th-cart-remove{background:none;border:none;color:var(--th-muted-foreground);font-size:18px;cursor:pointer;padding:0 2px;}',
      '.th-cart-foot{display:flex;align-items:center;justify-content:space-between;margin-top:12px;gap:12px;}',
      '.th-cart-total{display:flex;align-items:baseline;gap:8px;}',
      '.th-cart-checkout{background:var(--th-primary);color:var(--th-primary-foreground);border:none;border-radius:var(--th-radius-full);padding:10px 20px;font-weight:600;font-size:var(--th-font-size-sm);cursor:pointer;}',
      '@media (max-width:640px){.th-cart-panel{top:60px;right:8px;}}'
    ].join('');
    document.head.appendChild(style);
    document.addEventListener('click', function (e) {
      if (e.target && e.target.id === 'th-cart-close') toggleCart(false);
    });
    renderCartPanel();
  }

  /* ---------- 退出登录（右上角统一按钮） ---------- */
  function bindLogout() {
    var btn = document.getElementById('logout-btn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      Auth.logout();
      toast('已退出登录', 'info');
      setTimeout(function () { location.href = 'index.html'; }, 400);
    });
  }
  bindLogout();

  /* ---------- 初始化入口 ---------- */
  function init(options) {
    options = options || {};
    if (options.nav) renderNav(options.nav, options.active);
    if (options.footer) renderFooter(options.footer === true ? 'dark' : options.footer);
    if (options.nav) mountCartShell();
    bindCartEvents();
    updateCartBadge();
    refreshIcons();
  }

  global.TH = {
    init: init,
    toast: toast,
    esc: esc,
    fmtMoney: fmtMoney,
    refreshIcons: refreshIcons,
    Cart: Cart,
    Auth: Auth,
    MaterialCart: MaterialCart,
    updateCartBadge: updateCartBadge,
    renderCartPanel: renderCartPanel
  };
})(window);
