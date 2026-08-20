/* =========================================================
   TerraHalo (沃土之环) API 客户端
   统一对接 Flask 后端 REST API（session-cookie 认证）
   ========================================================= */
(function (global) {
  'use strict';

  // 后端地址：可通过 window.TH_API_BASE 覆盖（部署时修改）
  var API_BASE = global.TH_API_BASE || 'http://localhost:5000';
  var LS_USER = 'th_user';

  /* ---------- 底层请求封装 ---------- */
  function request(path, options) {
    options = options || {};
    options.method = options.method || 'GET';
    options.credentials = 'include'; // 跨端口携带 session cookie
    options.headers = Object.assign({}, options.headers || {});
    if (options.body && typeof options.body !== 'string') {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }
    return fetch(API_BASE + path, options).then(function (res) {
      return res.text().then(function (text) {
        var data = null;
        try { data = text ? JSON.parse(text) : null; } catch (e) { data = null; }
        if (!res.ok) {
          var err = new Error((data && data.error) || ('请求失败 (' + res.status + ')'));
          err.status = res.status;
          throw err;
        }
        return data;
      });
    });
  }

  /* ---------- URL 查询串 ---------- */
  function qs(params) {
    var parts = [];
    Object.keys(params || {}).forEach(function (k) {
      var v = params[k];
      if (v === undefined || v === null || v === '') return;
      parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
    });
    return parts.length ? '?' + parts.join('&') : '';
  }

  /* ---------- 认证 ---------- */
  var authApi = {
    login: function (username, password) {
      return request('/api/login', { method: 'POST', body: { username: username, password: password } });
    },
    register: function (payload) {
      return request('/api/register', { method: 'POST', body: payload });
    },
    logout: function () {
      // 后端 /logout 为 GET + redirect，仅用于清服务端 session
      try { fetch(API_BASE + '/logout', { credentials: 'include' }); } catch (e) { /* ignore */ }
      try { localStorage.removeItem(LS_USER); } catch (e) { /* ignore */ }
    },
    profile: function () { return request('/api/user/profile'); }
  };

  /* ---------- 原料 ---------- */
  var materialApi = {
    list: function (params) { return request('/api/materials' + qs(params)); },
    detail: function (id) { return request('/api/materials' + qs({ id: id })); }
  };

  /* ---------- 商品有机肥 ---------- */
  var productApi = {
    list: function (params) { return request('/api/products' + qs(params)); },
    detail: function (id) { return request('/api/products/' + id); }
  };

  /* ---------- 商品购物车（后端 session 存储） ---------- */
  var cartApi = {
    list: function () { return request('/api/product-cart'); },
    add: function (productId, qty) {
      return request('/api/product-cart/add', { method: 'POST', body: { product_id: productId, quantity: qty } });
    },
    remove: function (productId) {
      return request('/api/product-cart/remove', { method: 'POST', body: { product_id: productId } });
    },
    clear: function () { return request('/api/product-cart/clear', { method: 'POST' }); }
  };

  /* ---------- 商品订单 ---------- */
  var orderApi = {
    productList: function () { return request('/api/product-orders'); },
    productCreate: function (payload) { return request('/api/product-order/create', { method: 'POST', body: payload }); },
    productPay: function (id) { return request('/api/product-order/' + id + '/pay', { method: 'POST' }); },
    productCancel: function (id) { return request('/api/product-order/' + id + '/cancel', { method: 'POST' }); }
  };

  /* ---------- 管理后台（总控室，仅 admin） ---------- */
  var adminApi = {
    stats: function () { return request('/api/admin/stats'); },
    enterprises: function () { return request('/admin/api/admin/enterprises'); },
    enterpriseOverview: function () { return request('/admin/api/admin/enterprises/overview'); },
    drivers: function () { return request('/admin/api/admin/drivers'); },
    products: function (status) { return request('/admin/api/admin/products' + qs({ status: status })); },
    productStatus: function (id, status) {
      return request('/api/products/' + id + '/status', { method: 'POST', body: { status: status } });
    },
    users: function (role) { return request('/admin/api/audit/users' + qs({ role: role })); },
    toggleUser: function (id) {
      return request('/admin/api/audit/users/' + id + '/toggle-status', { method: 'POST' });
    },
    supplies: function (status) { return request('/admin/api/audit/supplies' + qs({ status: status })); },
    pendingTasks: function () { return request('/admin/api/dispatch/pending-tasks'); },
    dispatchDrivers: function () { return request('/admin/api/dispatch/drivers'); },
    assign: function (taskId, driverId) {
      return request('/admin/api/dispatch/assign', { method: 'POST', body: { task_id: taskId, driver_id: driverId } });
    }
  };

  global.TH_API = {
    base: API_BASE,
    auth: authApi,
    materials: materialApi,
    products: productApi,
    cart: cartApi,
    orders: orderApi,
    admin: adminApi,
    request: request,
    qs: qs
  };
})(window);
