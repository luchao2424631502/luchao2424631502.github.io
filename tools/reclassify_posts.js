#!/usr/bin/env node

/*
 * Rebuild the category hierarchy for recovered posts without changing titles,
 * dates, permalinks, tags, or article bodies.
 *
 * Usage:
 *   node tools/reclassify_posts.js          # preview only
 *   node tools/reclassify_posts.js --write  # update front matter
 */

'use strict';

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const postsDir = path.join(process.cwd(), 'source', '_posts');
const shouldWrite = process.argv.includes('--write');

function includesAny(text, expressions) {
  return expressions.some((expression) => expression.test(text));
}

function classifyAlgorithm(text) {
  if (includesAny(text, [
    /kmp/i, /manacher/i, /回文/, /字符串\s*hash/i, /trie/i, /拆分单词/,
  ])) {
    return ['算法与数据结构', '字符串算法'];
  }

  if (includesAny(text, [
    /欧拉图/, /最短路/i, /dijkstra|\bdij\b/i, /floyd/i, /spfa/i,
    /bellman/i, /kruskal/i, /\bprim\b|\bprime\b/i, /生成树/, /树形图/,
    /tarjan/i, /割点|割边|连通分量|双连通|强联通|缩点/, /最大匹配|二分图/,
    /\bkm\b|km算法/i, /最大流|最小割|dinic|edmonds|费用流|mcmf/i,
    /拓扑/, /最小路径覆盖|路径覆盖/, /最小环/, /hamilton/i, /highways/i,
    /建图/, /lca/i, /最大独立集|最大团/,
  ])) {
    return ['算法与数据结构', '图论'];
  }

  if (includesAny(text, [
    /并查集/, /食物链/, /发现环/, /线段树/, /splay/i, /treap/i,
    /替罪羊树/, /树状数组/, /\bst表\b|rmq/i, /块状链表/, /笛卡尔树/,
    /最小堆|\b堆\b/, /单调队列|单调栈/, /动态维护中位数/, /滑动窗口/,
    /huffman/i, /最优树/, /栈的应用/, /差分数组/,
  ])) {
    return ['算法与数据结构', '数据结构'];
  }

  if (includesAny(text, [
    /欧拉函数/, /质数|素数/, /扩展欧几里得/, /高斯消元/, /快速幂|快速乘/,
    /数论/, /matrix-tree/i,
  ])) {
    return ['算法与数据结构', '数学与数论'];
  }

  if (includesAny(text, [
    /动态规划|\bdp\b/i, /\bbfs\b|\bdfs\b/i, /枚举/, /瓷砖样式/,
    /调手表/, /uva\s*11624/i, /lcs/i, /最长上升子序列/, /爬楼梯/,
    /打家劫舍/, /最大连续子段和/, /hdu\s*1421/i,
  ])) {
    return ['算法与数据结构', '搜索与动态规划'];
  }

  return ['算法与数据结构', '基础算法'];
}

function classify(meta, filename) {
  const rawCategories = meta.categories == null
    ? []
    : (Array.isArray(meta.categories) ? meta.categories : [meta.categories]);
  const oldCategory = rawCategories.map(String).join(' > ');
  const tags = Array.isArray(meta.tags) ? meta.tags.join(' ') : String(meta.tags || '');
  const text = `${meta.title || ''} ${tags} ${filename}`;

  const taxonomyRoots = [
    '算法与数据结构', '编程语言', '系统与底层',
    '网络与服务', '工具与效率', 'Web开发', '站务',
  ];
  if (rawCategories.length === 2 && taxonomyRoots.includes(String(rawCategories[0]))) {
    return rawCategories.map(String);
  }

  if (oldCategory === '算法' || /欧拉图/.test(text)) {
    return classifyAlgorithm(text);
  }

  if (/matlab/i.test(text)) return ['编程语言', 'MATLAB'];
  if (/urllib|\bpy[_\s]|python/i.test(text)) return ['编程语言', 'Python'];

  if (/vim|neovim|emacs/i.test(text)) return ['工具与效率', '编辑器'];
  if (oldCategory === 'Makefile') return ['工具与效率', '构建与调试'];
  if (oldCategory === '编译链接') return ['编程语言', '编译与链接'];

  if (oldCategory === 'C++' || oldCategory === 'C++primer读书笔记') {
    return ['编程语言', 'C与C++'];
  }

  if (oldCategory === 'php') {
    return /css/i.test(text)
      ? ['Web开发', '前端']
      : ['Web开发', 'PHP与后端'];
  }

  if (oldCategory === '数据库(入门') return ['网络与服务', '数据库'];
  if (oldCategory === 'LDD') return ['系统与底层', '驱动与嵌入式'];
  if (oldCategory === 'X86实模式和保护模式') return ['系统与底层', 'x86与汇编'];

  if (oldCategory === '编写操作系统之路') {
    if (/att汇编/i.test(text)) return ['系统与底层', 'x86与汇编'];
    if (/lcd1602|intel\s*8042/i.test(text)) return ['系统与底层', '驱动与嵌入式'];
    if (/c语言提取tar/i.test(text)) return ['编程语言', 'C与C++'];
    return ['系统与底层', '自制操作系统'];
  }

  if (oldCategory === '操作系统') {
    if (/apue|标准io|文件io|文件和目录/i.test(text)) {
      return ['系统与底层', 'Unix系统编程'];
    }
    return ['系统与底层', '操作系统原理'];
  }

  if (oldCategory === '计算机网络') {
    if (/服务器|socket|http请求|i\/o复用|time_wait|标准io流/i.test(text)) {
      return ['网络与服务', '网络编程'];
    }
    return ['网络与服务', '计算机网络'];
  }

  if (oldCategory === 'Linux学习') {
    if (/shell|awk|cut|sed|正则表达式|重启mysql/i.test(text)) {
      return ['工具与效率', 'Shell与命令行'];
    }
    if (/select|recv|多播|广播|epoll|聊天室|unix域socket|httpserver/i.test(text)) {
      return ['网络与服务', '网络编程'];
    }
    if (/线程|mutex|条件变量|pthread|aio|进程中加载|apue/i.test(text)) {
      return ['系统与底层', 'Unix系统编程'];
    }
    if (/gcc|g\+\+|makefile/i.test(text)) return ['工具与效率', '构建与调试'];
    if (/dns|网络基础/i.test(text)) return ['网络与服务', '计算机网络'];
    if (/mysql|mariadb|wordpress/i.test(text)) return ['网络与服务', '数据库'];
    return ['系统与底层', 'Linux基础'];
  }

  throw new Error(`无法分类：${filename}（原分类：${oldCategory || '未分类'}）`);
}

function replaceCategories(raw, categories) {
  const match = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!match) throw new Error('缺少 YAML front matter');

  let header = match[1];
  const categoryBlock = /^categories:[ \t]*(?:\n(?:[ \t]*-[^\n]*\n?)*)?/m;
  header = header.replace(categoryBlock, '');
  header = header.replace(/\n{3,}/g, '\n\n').replace(/^\n|\n$/g, '');

  const lines = header.split('\n');
  const insertAt = lines.findIndex((line) => /^tags:/.test(line));
  const categoryLines = ['categories:', ...categories.map((category) => `- ${category}`)];
  if (insertAt >= 0) lines.splice(insertAt, 0, ...categoryLines);
  else lines.push(...categoryLines);

  return `---\n${lines.join('\n')}\n---\n\n${match[2].replace(/^\n+/, '')}`;
}

const files = fs.readdirSync(postsDir).filter((file) => file.endsWith('.md')).sort();
const counts = new Map();
let changed = 0;

for (const filename of files) {
  const filePath = path.join(postsDir, filename);
  const raw = fs.readFileSync(filePath, 'utf8');
  const match = raw.match(/^---\n([\s\S]*?)\n---/);
  if (!match) throw new Error(`缺少 YAML front matter：${filename}`);

  const meta = yaml.load(match[1]) || {};
  const categories = classify(meta, filename);
  const key = categories.join(' > ');
  counts.set(key, (counts.get(key) || 0) + 1);

  const updated = replaceCategories(raw, categories);
  if (updated !== raw) {
    changed += 1;
    if (shouldWrite) fs.writeFileSync(filePath, updated);
  }
}

console.log(`${shouldWrite ? '已更新' : '预计更新'} ${changed}/${files.length} 篇文章`);
for (const [category, count] of [...counts].sort((a, b) => a[0].localeCompare(b[0], 'zh-CN'))) {
  console.log(`${String(count).padStart(3)}  ${category}`);
}
