/* =========================================================
   TerraHalo (沃土之环) 共享模拟数据
   用于原料市场 / 有机肥商城 / 司机任务 等页面的渲染
   ========================================================= */
(function (global) {
  'use strict';

  // 图片资源（相对 assets/img）
  var IMG = {
    hero: 'assets/img/image_0_yi19x4.jpg',
    material: 'assets/img/image_1_yi19x4.jpg',
    product: 'assets/img/image_2_yi19x4.jpg'
  };

  // ---------- 原料市场 ----------
  var materials = [
    { id: 'm1', name: '鸡粪有机原料', category: 'chicken', categoryName: '鸡粪', weight: 50, location: '河北邢台', price: 180, time: '2小时前', status: 'pending', statusText: '待收购', img: IMG.material, desc: '优质鸡粪有机原料，来自规模化养殖场，经过初步堆肥发酵处理，含水率控制在30%以下，无沙石杂质，适合有机肥加工企业直接使用。长期供应，质量稳定。', supplier: '绿色农场', supplierLoc: '河北邢台', publishDate: '2026-06-25', cat: '禽畜粪便' },
    { id: 'm2', name: '牛粪发酵原料', category: 'cattle', categoryName: '牛粪', weight: 80, location: '山东济南', price: 120, time: '5小时前', status: 'transit', statusText: '运输中', img: IMG.material, desc: '规模化养牛场发酵牛粪，粗纤维含量高，经过高温堆肥无害化处理，适合生产生物有机肥与土壤改良剂。', supplier: '鲁西牧业', supplierLoc: '山东济南', publishDate: '2026-06-24', cat: '禽畜粪便' },
    { id: 'm3', name: '秸秆粉碎料', category: 'straw', categoryName: '秸秆', weight: 200, location: '河南周口', price: 60, time: '1天前', status: 'pending', statusText: '待收购', img: IMG.material, desc: '小麦与玉米秸秆混合粉碎料，颗粒均匀，含水率低，可用于有机肥辅料、生物质能源或反刍饲料加工。', supplier: '周口农合社', supplierLoc: '河南周口', publishDate: '2026-06-23', cat: '秸秆类' },
    { id: 'm4', name: '稻壳碳化料', category: 'other', categoryName: '其他', weight: 35, location: '江苏盐城', price: 220, time: '2天前', status: 'pending', statusText: '待收购', img: IMG.material, desc: '稻壳经低温碳化处理，孔隙发达，透气保水，是育苗基质与土壤改良的理想原料。', supplier: '盐城稻香合作社', supplierLoc: '江苏盐城', publishDate: '2026-06-22', cat: '其他' },
    { id: 'm5', name: '羊粪颗粒料', category: 'other', categoryName: '其他', weight: 45, location: '内蒙古赤峰', price: 150, time: '3天前', status: 'transit', statusText: '运输中', img: IMG.material, desc: '内蒙古草原散养羊粪，经造粒干燥处理，有机质丰富，缓释肥效，适合果树与蔬菜种植。', supplier: '赤峰草原牧业', supplierLoc: '内蒙古赤峰', publishDate: '2026-06-21', cat: '禽畜粪便' },
    { id: 'm6', name: '玉米芯颗粒', category: 'other', categoryName: '其他', weight: 120, location: '吉林四平', price: 90, time: '4天前', status: 'pending', statusText: '待收购', img: IMG.material, desc: '玉米芯粉碎造粒，吸水性强，可用作有机肥填充料、栽培基质或生物质颗粒原料。', supplier: '四平金穗合作社', supplierLoc: '吉林四平', publishDate: '2026-06-20', cat: '其他' },
    { id: 'm7', name: '猪粪发酵料', category: 'cattle', categoryName: '牛粪', weight: 60, location: '四川成都', price: 110, time: '6小时前', status: 'pending', statusText: '待收购', img: IMG.material, desc: '标准化养猪场猪粪，经固液分离与好氧发酵，重金属与病原菌达标，可直接用于有机肥生产。', supplier: '川西养殖联合体', supplierLoc: '四川成都', publishDate: '2026-06-19', cat: '禽畜粪便' },
    { id: 'm8', name: '花生壳粉', category: 'straw', categoryName: '秸秆', weight: 30, location: '山东临沂', price: 130, time: '8小时前', status: 'pending', statusText: '待收购', img: IMG.material, desc: '花生壳粉碎料，木质素含量适中，是食用菌栽培与有机肥发酵的良好辅料。', supplier: '临沂丰产合作社', supplierLoc: '山东临沂', publishDate: '2026-06-18', cat: '秸秆类' }
  ];

  // ---------- 有机肥商城 ----------
  var products = [
    { id: 'p1', name: '微生物菌剂有机肥', category: 'bio', categoryName: '生物有机肥', spec: '40kg/袋', specs: ['20kg/袋', '40kg/袋', '50kg/袋'], price: 89, originalPrice: 120, rating: 4.9, sold: 2386, img: IMG.product, desc: '本产品采用优质农业废弃物经微生物深度发酵而成，富含有机质和多种有益微生物菌群。适用于水稻、小麦、玉米、蔬菜等多种农作物，可有效改良土壤结构，提升土壤肥力，促进作物根系发育。', crops: ['水稻', '小麦', '玉米', '蔬菜'] },
    { id: 'p2', name: '复合微生物肥料', category: 'compound', categoryName: '复合微生物肥', spec: '25kg/袋', specs: ['25kg/袋', '50kg/袋'], price: 128, originalPrice: 158, rating: 4.6, sold: 1852, img: IMG.product, desc: '多种功能菌群复配，兼具解磷解钾与促生功能，配合有机质载体，肥效持久稳定。', crops: ['水稻', '玉米', '大豆'] },
    { id: 'p3', name: '生物有机肥', category: 'bio', categoryName: '生物有机肥', spec: '50kg/袋', specs: ['25kg/袋', '50kg/袋'], price: 76, originalPrice: 96, rating: 4.8, sold: 3210, img: IMG.product, desc: '以畜禽粪便为主料，经完全腐熟无害化处理，有机质含量高，适用于大田作物基肥。', crops: ['小麦', '玉米', '蔬菜'] },
    { id: 'p4', name: '土壤调理剂', category: 'soil', categoryName: '土壤调理剂', spec: '20kg/袋', specs: ['20kg/袋', '40kg/袋'], price: 156, originalPrice: 189, rating: 4.7, sold: 1045, img: IMG.product, desc: '针对酸化、板结土壤研发，富含硅钙镁等中微量元素，改善土壤理化性状。', crops: ['蔬菜', '果树', '水稻'] },
    { id: 'p5', name: '腐殖酸有机肥', category: 'bio', categoryName: '生物有机肥', spec: '40kg/袋', specs: ['20kg/袋', '40kg/袋'], price: 98, originalPrice: 128, rating: 4.5, sold: 896, img: IMG.product, desc: '腐殖酸与有机质协同增效，促进根系发育，提高养分利用率。', crops: ['玉米', '大豆', '果树'] },
    { id: 'p6', name: '氨基酸水溶肥', category: 'compound', categoryName: '复合微生物肥', spec: '10L/桶', specs: ['5L/桶', '10L/桶'], price: 135, originalPrice: 165, rating: 4.8, sold: 1523, img: IMG.product, desc: '氨基酸螯合态养分，易吸收，适合滴灌、冲施，快速补充作物营养。', crops: ['蔬菜', '果树', '花卉'] }
  ];

  // ---------- 司机任务 ----------
  var driverTasks = {
    pending: [
      { id: 't1', from: '建邺区', to: '江宁区', type: '餐厨垃圾', weight: '2 吨', fee: 180, deadline: '14:30' },
      { id: 't2', from: '鼓楼区', to: '栖霞区', type: '园林垃圾', weight: '3 吨', fee: 240, deadline: '16:00' },
      { id: 't3', from: '玄武区', to: '浦口区', type: '生活垃圾', weight: '1.5 吨', fee: 150, deadline: '17:30' }
    ],
    active: [
      { id: 'a1', from: '秦淮区', to: '雨花台区', type: '餐厨垃圾', weight: '4 吨', fee: 320 }
    ],
    done: [
      { id: 'd1', place: '江宁区', type: '餐厨垃圾', weight: '2 吨', date: '2026-06-25', fee: 180 },
      { id: 'd2', place: '栖霞区', type: '园林垃圾', weight: '3 吨', date: '2026-06-24', fee: 240 },
      { id: 'd3', place: '浦口区', type: '生活垃圾', weight: '1.5 吨', date: '2026-06-24', fee: 150 },
      { id: 'd4', place: '建邺区', type: '餐厨垃圾', weight: '2.5 吨', date: '2026-06-23', fee: 200 },
      { id: 'd5', place: '鼓楼区', type: '园林垃圾', weight: '2 吨', date: '2026-06-22', fee: 180 }
    ]
  };

  // ---------- 企业工作台 ----------
  var enterprise = {
    kpi: [
      { label: '采购需求', value: '12', badge: '进行中', badgeType: 'success' },
      { label: '收运任务', value: '5', badge: '运输中', badgeType: 'neutral' },
      { label: '上架商品', value: '28', badge: null },
      { label: '本月交易额', value: '¥128,500', badge: null }
    ],
    todos: [
      { title: '待匹配需求', sub: '3条采购需求待匹配' },
      { title: '待派单任务', sub: '2个收运任务待派单' },
      { title: '待结算订单', sub: '6笔订单待结算' }
    ],
    tasks: [
      { code: '#TSK-2406', type: '鸡粪', driver: '王师傅', status: '已完成', statusType: 'success', date: '06-25' },
      { code: '#TSK-2407', type: '猪粪', driver: '李师傅', status: '运输中', statusType: 'neutral', date: '06-25' },
      { code: '#TSK-2408', type: '牛粪', driver: '赵师傅', status: '运输中', statusType: 'neutral', date: '06-24' },
      { code: '#TSK-2409', type: '秸秆', driver: '陈师傅', status: '已完成', statusType: 'success', date: '06-23' }
    ]
  };

  global.TH_DATA = {
    IMG: IMG,
    materials: materials,
    products: products,
    driverTasks: driverTasks,
    enterprise: enterprise
  };
})(window);
