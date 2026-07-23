<template>
  <MobileDrawer v-model="isMobileMenuOpen" subtitle="项目、教程、仓库和 Live Demo">
    <p>欢迎来到「爬楼的猪 Dev」</p>
    <p>项目、教程、仓库、Live Demo ... ...</p>
  </MobileDrawer>

  <HeaderBar :route-name="'首页'" :scroll="true" @toggle-mobile-menu="onToggleMobileMenu" />

  <div class="home-page">
    <div class="interaction-glow" :style="glowStyle" aria-hidden="true"></div>
    <main class="home-main">
      <section class="hero-section" aria-labelledby="home-title">
        <div class="hero-copy">
          <h1 id="home-title" class="hero-title">
            <span class="hero-title__emoji" aria-hidden="true">🎉</span>
            <span class="hero-title__text">欢迎来到</span>
            <span class="hero-title__pill">爬楼的猪 <strong>Dev</strong></span>
          </h1>
          <p class="hero-subtitle">项目教程 &amp; Live Demo</p>
          <p class="hero-description">分享和记录一些我个人在做的，感兴趣的工具和内容 😁</p>

          <div class="hero-actions">
            <a class="button-primary hero-button" href="/articles">查看项目教程</a>
            <a
              class="button-ghost hero-button"
              href="/livedemo"
              data-analytics-cta="live_demo"
              data-analytics-source="home.hero"
              data-analytics-label="查看 Demo / GitHub"
            >
              查看 Demo / GitHub
            </a>
          </div>

          <!-- <ul class="hero-points">
            <li>开发里的零散内容，慢慢放到这里</li>
            <li>能复用的、能跑的、顺手能查的，会优先留下来</li>
          </ul> -->
        </div>

        <aside class="hero-index" aria-label="首页内容索引">
          <a class="index-card index-card--tutorial" :href="featuredSeries.tutorialLink || '/articles'">
            <span class="index-card__label">Latest Tutorial</span>
            <strong>{{ featuredSeries.title || "未命名专栏" }}</strong>
            <span>{{ featuredSeries.description || "暂无描述" }}</span>
          </a>
          <a
            class="index-card index-card--demo"
            :href="featuredDemo.demoLink || '/livedemo'"
            target="_blank"
            rel="noopener noreferrer"
            data-analytics-cta="live_demo"
            data-analytics-source="home.featured_demo"
            :data-analytics-label="featuredDemo.title || '在线体验'"
          >
            <span class="index-card__label">Live Demo</span>
            <strong>{{ featuredDemo.title || "未命名 Demo" }}</strong>
            <span>{{ featuredDemo.description || "暂无描述" }}</span>
          </a>
          <a class="index-card index-card--reading" :href="secondarySeries.tutorialLink || '/articles'">
            <span class="index-card__label">More Reading</span>
            <strong>{{ secondarySeries.title || "未命名专栏" }}</strong>
            <span>{{ secondarySeries.description || "暂无描述" }}</span>
          </a>
        </aside>
      </section>

      <section class="demo-lab-section" aria-labelledby="demo-lab-title">
        <div class="section-heading section-heading--lab">
          <div>
            <p class="section-kicker">Live Demo</p>
            <h2 id="demo-lab-title">在线体验</h2>
          </div>
          <div class="section-heading-side">
            <a class="section-link" href="/livedemo">全部 Demo<span class="link-arrow" aria-hidden="true"></span></a>
          </div>
        </div>

        <div class="demo-workbench" aria-label="Demo workspace">
          <div class="ide-titlebar">
            <span class="ide-dot ide-dot--red"></span>
            <span class="ide-dot ide-dot--yellow"></span>
            <span class="ide-dot ide-dot--green"></span>
            <span>{{ selectedDemoPathLabel }}</span>
          </div>

          <div class="ide-body">
            <aside class="demo-rail" aria-label="Demo 文件列表">
              <button
                v-for="(demo, index) in demos"
                :key="demo.id"
                type="button"
                :class="['demo-tab', { 'demo-tab--active': index === activeDemoIndex }]"
                @click="setActiveDemo(index)"
              >
                <span class="demo-tab__number">{{ formatNumber(index + 1) }}</span>
                <span class="demo-tab__copy">
                  <strong>{{ demo.title }}</strong>
                  <span>demos/{{ getDemoSlug(demo) }}/preview.html</span>
                </span>
                <span :class="['demo-tab__status', `demo-tab__status--${demo.status}`]">{{ demo.status === "done" ? "online" : "draft" }}</span>
              </button>
            </aside>

            <div class="lab-stage">
              <div class="ide-tabs" aria-hidden="true">
                <span class="ide-tab ide-tab--active">README.md</span>
                <span class="ide-tab">preview.html</span>
                <span class="ide-tab">launch.json</span>
                <span class="ide-tab">...</span>
              </div>

              <div class="ide-canvas">
                <article class="ide-editor" aria-label="Demo README">
                  <div class="editor-path">live-demo / {{ selectedDemoSlug }} / README.md</div>
                  <pre><code><span v-for="line in selectedDemoReadmeLines" :key="line.no" class="editor-line"><span>{{ line.no }}</span><b>{{ line.text }}</b></span></code></pre>
                  <div class="editor-actions">
                    <a
                      class="button-primary button-small"
                      :href="selectedDemo.demoLink"
                      target="_blank"
                      rel="noopener noreferrer"
                      data-analytics-cta="live_demo"
                      :data-analytics-source="`home.demo_ide.${selectedDemo.id || selectedDemo.title || 'unknown'}`"
                      :data-analytics-label="selectedDemo.title || '在线体验'"
                    >
                      在线打开
                    </a>
                    <a class="button-ghost button-small" :href="selectedDemo.repoLink" target="_blank" rel="noopener noreferrer">GitHub</a>
                  </div>
                </article>

                <a
                  class="ide-preview"
                  :href="selectedDemo.demoLink || '/livedemo'"
                  target="_blank"
                  rel="noopener noreferrer"
                  data-analytics-cta="live_demo"
                  :data-analytics-source="`home.demo_ide.preview.${selectedDemo.id || selectedDemo.title || 'unknown'}`"
                  :data-analytics-label="selectedDemo.title || '在线体验'"
                >
                  <div class="preview-toolbar">
                    <span>{{ selectedDemoPathLabel }}</span>
                    <strong>{{ selectedDemo.status === "done" ? "running" : "preview" }}</strong>
                  </div>
                  <div class="preview-frame">
                    <img v-if="selectedDemoPreviewSrc" :src="selectedDemoPreviewSrc" :alt="selectedDemo.title" />
                    <div v-else class="result-placeholder" aria-hidden="true">{{ demoInitials }}</div>
                  </div>
                </a>
              </div>

              <div class="ide-statusbar" aria-hidden="true">
                <span>{{ selectedDemo.title || "未命名 Demo" }}</span>
                <span>{{ selectedDemoRepoLabel }}</span>
                <span>ready</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="blog-section" aria-labelledby="blog-title">
        <div class="section-heading">
          <div>
            <p class="section-kicker">Blog</p>
            <h2 id="blog-title">文章</h2>
          </div>
          <div class="section-heading-side">
            <a class="section-link" href="/articles">全部文章<span class="link-arrow" aria-hidden="true"></span></a>
          </div>
        </div>

        <div class="featured-reading">
          <article v-for="article in hotArticles" :key="article.id" class="article-row">
            <a class="article-cover" :href="article.tutorialLink" aria-hidden="true" tabindex="-1">
              <img :src="article.cover" :alt="article.title" loading="lazy" decoding="async" />
            </a>
            <div class="article-copy">
              <div class="article-meta">
                <span>{{ article.category || article.tags?.[0] || "文章" }}</span>
                <span v-if="article.date">{{ article.date }}</span>
              </div>
              <h3>
                <a :href="article.tutorialLink">{{ article.title }}</a>
              </h3>
              <p>{{ article.description }}</p>
              <div class="article-bottom">
                <div class="tag-list">
                  <span v-for="tag in article.tags" :key="tag" class="tag-chip">{{ tag }}</span>
                </div>
                <a class="text-link" :href="article.tutorialLink">看教程<span class="link-arrow" aria-hidden="true"></span></a>
              </div>
            </div>
          </article>
        </div>
      </section>

      <section class="about-panel">
        <div class="about-avatar">
          <img :src="'/api/v1/website/image/avatar/admin.jpg'" alt="about avatar" />
        </div>
        <div class="about-copy">
          <h2>关于我</h2>
          <p>爬楼的猪 · 平时写点项目、工具脚本、博客笔记</p>
          <p>CSDN主页: <a href="https://blog.csdn.net/pldz1" target="_blank" rel="noopener noreferrer">https://blog.csdn.net/pldz1</a></p>
        </div>
        <a class="button-ghost button-small" :href="githubLink">Github 主页<span class="link-arrow" aria-hidden="true"></span></a>
      </section>
    </main>

    <FooterBar />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import FooterBar from "../components/FooterBar.vue";
import HeaderBar from "../components/HeaderBar.vue";
import MobileDrawer from "../components/MobileDrawer.vue";
import { getAllLiveDemos, getAllArticles, getArticleIntros } from "../utils/apis";

const isMobileMenuOpen = ref(false);
const activeDemoIndex = ref(0);
const pointerX = ref(0);
const pointerY = ref(0);

const series = ref([]);
const hotArticles = ref([]);
const demos = ref([]);

const githubLink = "https://github.com/pldz1";

const featuredSeries = computed(() => series.value[0] || {});
const secondarySeries = computed(() => series.value[1] || {});
const featuredDemo = computed(() => demos.value[0] || {});
const selectedDemo = computed(() => demos.value[activeDemoIndex.value] || featuredDemo.value || {});

const demoInitials = computed(() =>
  String(selectedDemo.value?.title || "Demo")
    .slice(0, 2)
    .toUpperCase()
);
const selectedDemoSlug = computed(() => getDemoSlug(selectedDemo.value));
const selectedDemoPathLabel = computed(() => getDemoPathLabel(selectedDemo.value?.demoLink, `/io/${selectedDemoSlug.value}/`));
const selectedDemoRepoLabel = computed(() => getLinkLabel(selectedDemo.value?.repoLink, "GitHub"));
const selectedDemoPreviewSrc = computed(() => selectedDemo.value?.previewgif || selectedDemo.value?.thumbnail || "");
const selectedDemoReadmeLines = computed(() => {
  const demo = selectedDemo.value || {};
  const lines = [
    `# ${demo.title || "未命名 Demo"}`,
    "",
    `status: ${demo.status === "done" ? "online" : demo.status || "preview"}`,
    `route: ${selectedDemoPathLabel.value}`,
    `source: ${selectedDemoRepoLabel.value}`,
    "",
    "## what to try",
    demo.description || "打开预览，确认这个小工具是否值得继续展开。",
    "",
    "## workspace",
    `live-demo/${selectedDemoSlug.value}/preview.html`,
    `live-demo/${selectedDemoSlug.value}/README.md`,
  ];

  return lines.map((text, index) => ({
    no: String(index + 1).padStart(2, "0"),
    text,
  }));
});

const glowStyle = computed(() => ({
  "--mx": `${pointerX.value}px`,
  "--my": `${pointerY.value}px`,
}));

function formatNumber(value) {
  return String(value).padStart(2, "0");
}

function getDemoSlug(demo) {
  const raw = demo?.id || demo?.folder || demo?.title || "demo";
  return (
    String(raw)
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, "-")
      .replace(/^-+|-+$/g, "") || "demo"
  );
}

function getLinkLabel(link, fallback) {
  if (!link) return fallback;
  try {
    const url = new URL(link, window.location.origin);
    return url.hostname === window.location.hostname ? url.pathname || fallback : url.hostname;
  } catch {
    return fallback;
  }
}

function getDemoPathLabel(link, fallback) {
  if (!link) return fallback;
  if (String(link).startsWith("/")) return link;
  try {
    const url = new URL(link, window.location.origin);
    return `${url.pathname}${url.search}${url.hash}` || fallback;
  } catch {
    return fallback;
  }
}

function setActiveDemo(index) {
  activeDemoIndex.value = index;
}

function uniqueBy(items, getKey) {
  const seen = new Set();
  return items.filter((item, index) => {
    const key = String(getKey(item, index) || "")
      .trim()
      .toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function normalizeTags(tags) {
  if (Array.isArray(tags)) return tags.filter(Boolean).slice(0, 4);
  if (typeof tags === "string") {
    return tags
      .split(/[,\s]+/)
      .map((item) => item.trim())
      .filter(Boolean)
      .slice(0, 4);
  }
  return [];
}

function normalizeSeriesCard(article, index) {
  const category = article?.category || "";
  const seriesLink = category ? `/articles/${encodeURIComponent(category)}` : "/articles";

  return {
    id: category || article?.id || `project-${index}`,
    title: article?.title || "未命名专栏",
    description: article?.summary || "暂无描述",
    cover: article?.thumbnail || "",
    tags: normalizeTags(article?.tags),
    tutorialLink: seriesLink,
    repoLink: article?.github || article?.gitee || article?.csdn || seriesLink,
  };
}

function normalizeHotArticle(article, index) {
  const articleLink = article?.id ? `/article/${article.id}` : "/articles";

  return {
    id: article?.id || `hot-article-${index}`,
    title: article?.title || "未命名文章",
    description: article?.summary || "暂无描述",
    cover: article?.thumbnail || "/404.jpg",
    tags: normalizeTags(article?.tags),
    category: article?.category || "",
    date: article?.date || "",
    tutorialLink: articleLink,
    repoLink: article?.github || article?.gitee || article?.csdn || articleLink,
  };
}

function normalizeLiveDemo(item, index) {
  const url = item?.url || "";
  const sourceLink = item?.sourcelink || item?.url || "https://github.com";
  return {
    id: item?.folder || item?.title || `demo-${index}`,
    title: item?.title || "未命名 Demo",
    description: item?.description || "暂无描述",
    status: "done",
    demoLink: url,
    repoLink: sourceLink,
    thumbnail: item?.thumbnail || "",
    previewgif: item?.previewgif || "",
  };
}

async function loadHomeData() {
  const [articlesRes, articleIntrosRes, livedemoRes] = await Promise.allSettled([getAllArticles(), getArticleIntros(), getAllLiveDemos()]);

  const articles = articlesRes.status === "fulfilled" && Array.isArray(articlesRes.value) ? articlesRes.value : [];
  const articleIntros = articleIntrosRes.status === "fulfilled" && Array.isArray(articleIntrosRes.value) ? articleIntrosRes.value : [];
  const livedemos = livedemoRes.status === "fulfilled" && Array.isArray(livedemoRes.value) ? livedemoRes.value : [];

  const uniqueArticles = uniqueBy(articles, (article, index) => article?.title || article?.id || `article-${index}`);
  const uniqueArticleIntros = uniqueBy(articleIntros, (article, index) => article?.category || article?.title || `series-${index}`);
  const uniqueLiveDemos = uniqueBy(livedemos, (demo, index) => demo?.folder || demo?.title || demo?.url || `demo-${index}`);

  const sortedArticles = [...uniqueArticles].sort((a, b) => String(b?.date || "").localeCompare(String(a?.date || "")));
  const sortedSeries = [...uniqueArticleIntros].sort((a, b) => String(b?.date || "").localeCompare(String(a?.date || "")));

  const seriesCards = sortedSeries
    .filter((article) => article?.category || article?.title)
    .slice(0, 3)
    .map(normalizeSeriesCard);

  const hotArticleCards = sortedArticles
    .filter((article) => article?.id && article?.title)
    .slice(0, 3)
    .map(normalizeHotArticle);

  const demoCards = uniqueLiveDemos.slice(0, 4).map(normalizeLiveDemo);

  series.value = seriesCards.length ? seriesCards : [];
  hotArticles.value = hotArticleCards.length ? hotArticleCards : [];
  demos.value = demoCards.length ? demoCards : [];
  activeDemoIndex.value = 0;
}

function onToggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
}

function onCloseMobileMenu() {
  isMobileMenuOpen.value = false;
}

function onResize() {
  if (window.innerWidth > 840) {
    onCloseMobileMenu();
  }
}

function onPointerMove(event) {
  pointerX.value = event.clientX;
  pointerY.value = event.clientY;
}

onMounted(() => {
  pointerX.value = window.innerWidth * 0.64;
  pointerY.value = window.innerHeight * 0.36;
  window.addEventListener("resize", onResize);
  window.addEventListener("pointermove", onPointerMove, { passive: true });
  loadHomeData();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize);
  window.removeEventListener("pointermove", onPointerMove);
});
</script>

<style scoped>
:global(body) {
  background: radial-gradient(circle at top left, color-mix(in srgb, var(--accent) 8%, transparent), transparent 34rem),
    linear-gradient(180deg, var(--app-bg), var(--app-bg));
  color: var(--app-text);
}

.home-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.interaction-glow {
  position: fixed;
  z-index: 0;
  left: calc(var(--mx) - 190px);
  top: calc(var(--my) - 190px);
  width: 380px;
  height: 380px;
  border-radius: 999px;
  background: radial-gradient(
    circle,
    color-mix(in srgb, var(--accent) 13%, transparent),
    color-mix(in srgb, var(--app-green) 5%, transparent) 42%,
    transparent 70%
  );
  filter: blur(18px);
  opacity: 0.72;
  pointer-events: none;
  transition: left 120ms var(--app-ease), top 120ms var(--app-ease);
}

.home-main {
  position: relative;
  z-index: 1;
  width: min(1160px, calc(100% - 40px));
  margin: 0 auto;
  padding: 76px 0 50px;
}

.hero-section {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(340px, 0.46fr);
  gap: 26px;
  align-items: start;
  min-height: 0;
  padding: 8px 0 24px;
}

.hero-copy {
  min-width: 0;
  padding: 64px 8px;
}

.section-kicker {
  margin: 0 0 16px;
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.18em;
  line-height: 1;
  text-transform: uppercase;
}

.hero-title {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin: 0;
  color: var(--app-text);
  font-family: var(--font-sans);
  font-size: clamp(30px, 3.35vw, 44px);
  font-weight: 900;
  line-height: 1.02;
  letter-spacing: 0;
}

.hero-title__emoji {
  line-height: 1;
  transform: translateY(2px);
}

.hero-title__text,
.hero-title__pill {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.hero-title__pill {
  padding: 0.06em 0.34em 0.12em;
  border: 2px solid color-mix(in srgb, var(--app-text) 88%, transparent);
  border-radius: 13px;
  background: var(--app-surface);
  box-shadow: 4px 4px 0 color-mix(in srgb, var(--accent) 22%, transparent);
}

.hero-title__pill strong {
  margin-left: 0.18em;
  font-weight: 900;
}

.hero-subtitle {
  margin: 16px 0 0;
  color: color-mix(in srgb, var(--accent) 72%, var(--app-text));
  font-size: 17px;
  font-weight: 650;
  line-height: 1.5;
}

.hero-description {
  max-width: 580px;
  margin: 12px 0 0;
  color: var(--app-text-muted);
  font-size: 15px;
  line-height: 1.78;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
}

.hero-button {
  height: 40px;
  padding: 0 16px;
}

.hero-points {
  display: grid;
  gap: 10px;
  max-width: 540px;
  margin: 18px 0 0;
  padding: 0;
  list-style: none;
}

.hero-points li {
  position: relative;
  padding-left: 22px;
  color: var(--app-text-muted);
  font-size: 15px;
  line-height: 1.75;
}

.hero-points li::before {
  content: "";
  position: absolute;
  top: 0.78em;
  left: 0;
  width: 8px;
  height: 8px;
  border: 2px solid var(--accent);
  border-radius: 999px;
  background: var(--app-surface);
}

.hero-index {
  position: relative;
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  padding: 10px;
  border: 1px solid color-mix(in srgb, var(--accent) 18%, var(--app-border));
  border-radius: 18px;
  background: color-mix(in srgb, var(--app-surface) 84%, transparent);
  box-shadow: var(--app-shadow-sm);
}

.hero-index::before {
  display: none;
}

.index-card {
  position: relative;
  display: grid;
  gap: 8px;
  min-height: 84px;
  padding: 13px 14px 13px 30px;
  border: 1px solid var(--app-border);
  border-radius: 12px;
  background: color-mix(in srgb, var(--app-surface) 94%, transparent);
  color: inherit;
  text-decoration: none;
  box-shadow: none;
}

.index-card::before {
  content: "";
  position: absolute;
  top: 22px;
  left: 13px;
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: var(--index-accent, var(--accent));
  box-shadow: 0 0 0 5px color-mix(in srgb, var(--index-accent, var(--accent)) 14%, transparent);
}

.index-card--tutorial {
  --index-accent: var(--accent);
}

.index-card--demo {
  --index-accent: var(--app-green);
}

.index-card--reading {
  --index-accent: var(--app-orange);
}

.index-card:hover {
  border-color: color-mix(in srgb, var(--index-accent, var(--accent)) 42%, var(--app-border));
  transform: translateY(-2px);
}

.index-card__label {
  color: var(--app-text-soft);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.index-card strong {
  color: var(--app-text);
  font-size: 16px;
  line-height: 1.35;
}

.index-card > span:last-child {
  display: -webkit-box;
  overflow: hidden;
  color: var(--app-text-muted);
  line-height: 1.65;
  font-size: 14px;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 24px;
  margin-bottom: 20px;
}

.section-heading h2,
.about-copy h2 {
  margin: 0;
  color: var(--app-text);
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 1.2;
}

.section-heading h2 {
  font-size: 30px;
  letter-spacing: -0.02em;
}

.section-heading-side {
  display: grid;
  justify-items: end;
  gap: 10px;
}

.section-link,
.text-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--accent);
  text-decoration: none;
  font-weight: 650;
}

.section-link {
  font-size: 14px;
}

.link-arrow {
  width: 16px;
  height: 16px;
  flex: 0 0 auto;
  background: currentColor;
  mask: url("../assets/svgs/arrow-right-16.svg") center / contain no-repeat;
  -webkit-mask: url("../assets/svgs/arrow-right-16.svg") center / contain no-repeat;
  transform: translateY(1px);
}

.demo-lab-section {
  position: relative;
  margin: 0 0 48px;
  padding: 24px;
  border: 1px solid color-mix(in srgb, var(--accent) 28%, var(--app-border));
  border-radius: 18px;
  background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 7%, transparent), transparent 210px),
    repeating-linear-gradient(90deg, transparent 0 31px, color-mix(in srgb, var(--app-border) 42%, transparent) 31px 32px),
    linear-gradient(180deg, color-mix(in srgb, var(--app-surface) 96%, transparent), var(--app-surface));
  box-shadow: none;
}

.demo-lab-section::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--app-green) 18%, transparent), transparent);
  opacity: 0.24;
  transform: translateX(-72%);
  animation: labSweep 7s ease-in-out infinite;
  pointer-events: none;
}

.section-heading--lab {
  position: static;
  margin: 0 0 20px;
  padding: 0;
  background: transparent;
}

.demo-workbench {
  display: grid;
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--app-text) 22%, var(--app-border));
  border-radius: 16px;
  background: #111827;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.14);
}

.ide-titlebar {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 40px;
  padding: 0 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(248, 251, 255, 0.72);
  font-size: 12px;
}

.ide-titlebar strong {
  margin-left: 6px;
  color: #f8fbff;
  font-family: var(--font-mono);
  font-size: 12px;
}

.ide-titlebar > span:last-child {
  margin-left: auto;
  overflow: hidden;
  color: rgba(248, 251, 255, 0.52);
  font-family: var(--font-mono);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ide-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.ide-dot--red {
  background: #ff6b6b;
}

.ide-dot--yellow {
  background: #ffd166;
}

.ide-dot--green {
  background: #63d297;
}

.ide-body {
  display: grid;
  grid-template-columns: minmax(230px, 0.27fr) minmax(0, 1fr);
  height: clamp(470px, 39vw, 510px);
  min-height: 0;
}

.demo-rail {
  display: grid;
  align-content: start;
  gap: 6px;
  min-width: 0;
  min-height: 0;
  padding: 12px 10px;
  overflow: auto;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  background: #0f1724;
}

.demo-tab {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 9px;
  width: 100%;
  min-height: 58px;
  padding: 9px;
  border: 1px solid transparent;
  border-radius: 10px;
  background: transparent;
  color: rgba(248, 251, 255, 0.82);
  text-align: left;
  cursor: pointer;
  box-shadow: none;
}

.demo-tab:hover,
.demo-tab--active {
  border-color: rgba(112, 232, 255, 0.2);
  background: rgba(255, 255, 255, 0.07);
  box-shadow: inset 3px 0 0 #70e8ff;
  transform: none;
}

.demo-tab--active .demo-tab__number {
  animation: numberPulse 1.45s ease-in-out infinite;
}

.demo-tab__number {
  color: #63d297;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 800;
}

.demo-tab__copy {
  display: grid;
  min-width: 0;
  gap: 6px;
}

.demo-tab__copy strong {
  overflow: hidden;
  color: #f8fbff;
  font-size: 13px;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.demo-tab__copy span {
  overflow: hidden;
  color: rgba(248, 251, 255, 0.5);
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 1.45;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.demo-tab__status {
  grid-column: 2;
  justify-self: start;
  padding: 3px 7px;
  border: 1px solid rgba(99, 210, 151, 0.28);
  border-radius: 999px;
  color: #63d297;
  font-family: var(--font-mono);
  font-size: 10px;
}

.lab-stage {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  min-width: 0;
  min-height: 0;
  background: radial-gradient(circle at 78% 12%, rgba(112, 232, 255, 0.09), transparent 30%), #111827;
}

.ide-tabs {
  display: flex;
  min-width: 0;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.ide-tab {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 14px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(248, 251, 255, 0.54);
  font-family: var(--font-mono);
  font-size: 12px;
}

.ide-tab--active {
  background: rgba(255, 255, 255, 0.06);
  color: #f8fbff;
}

.ide-canvas {
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(300px, 0.72fr);
  gap: 12px;
  min-height: 0;
  padding: 14px;
}

.ide-editor,
.ide-preview {
  min-height: 0;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  background: rgba(15, 23, 36, 0.72);
}

.ide-editor {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-width: 0;
  min-height: 0;
}

.editor-path,
.preview-toolbar {
  min-height: 34px;
  padding: 0 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(248, 251, 255, 0.56);
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 34px;
}

.ide-editor pre {
  margin: 0;
  padding: 14px 0;
  min-height: 0;
  overflow: auto;
}

.ide-editor code {
  display: grid;
  gap: 2px;
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 1.68;
}

.editor-line {
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr);
  gap: 12px;
  padding: 0 14px;
  align-items: center;
}

.editor-line span {
  color: rgba(248, 251, 255, 0.28);
  text-align: right;
}

.editor-line b {
  overflow: hidden;
  color: #d9e7ff;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: pre-wrap;
}

.editor-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.ide-preview {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  min-width: 0;
  color: inherit;
  text-decoration: none;
}

.preview-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  line-height: 1;
}

.preview-toolbar strong {
  color: #63d297;
  font-size: 11px;
}

.preview-frame {
  display: grid;
  min-height: 0;
  padding: 14px;
  background: linear-gradient(135deg, rgba(112, 232, 255, 0.08), transparent 40%), rgba(248, 251, 255, 0.03);
  place-items: center;
}

.preview-frame img {
  width: 100%;
  max-height: 100%;
  object-fit: contain;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  box-shadow: 0 22px 46px rgba(0, 0, 0, 0.22);
  transition: transform 260ms var(--app-ease);
}

.ide-preview:hover .preview-frame img {
  transform: translateY(-2px) scale(1.01);
}

.result-placeholder {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 96px;
  border: 1px solid color-mix(in srgb, var(--app-green) 34%, var(--app-border));
  border-radius: 22px;
  background: var(--app-surface);
  color: var(--app-green);
  font-size: 20px;
  font-weight: 800;
}

.ide-statusbar {
  display: flex;
  gap: 18px;
  align-items: center;
  min-height: 30px;
  padding: 0 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: #0f1724;
  color: rgba(248, 251, 255, 0.52);
  font-family: var(--font-mono);
  font-size: 11px;
}

.ide-statusbar span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ide-statusbar span:last-child {
  margin-left: auto;
  color: #63d297;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--app-text-soft);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.article-copy h3 {
  margin: 0;
  color: var(--app-text);
  font-size: 19px;
  line-height: 1.35;
}

.article-copy p,
.about-copy p {
  margin: 0;
  color: var(--app-text-muted);
  line-height: 1.75;
}

.article-bottom,
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.blog-section {
  margin-bottom: 48px;
}

.featured-reading {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.article-row {
  display: grid;
  grid-template-rows: auto 1fr;
  min-width: 0;
  overflow: hidden;
  border: 1px solid var(--app-border);
  border-radius: 12px;
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
  transition: border-color 180ms var(--app-ease), box-shadow 180ms var(--app-ease), transform 180ms var(--app-ease);
}

.article-cover {
  display: block;
  overflow: hidden;
  aspect-ratio: 16 / 9;
  border-bottom: 1px solid var(--app-border);
  background: var(--app-surface-sunken);
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 220ms var(--app-ease);
}

.article-row:hover {
  border-color: color-mix(in srgb, var(--accent) 34%, var(--app-border));
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.1);
  transform: translateY(-2px);
}

.article-row:hover .article-cover img {
  transform: scale(1.035);
}

.article-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
  gap: 10px;
  padding: 16px;
}

.article-copy h3 a {
  color: inherit;
  text-decoration: none;
}

.article-copy h3 a:hover {
  color: var(--accent);
}

.article-copy p {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  font-size: 14px;
}

.article-bottom {
  align-items: flex-start;
  flex-direction: column;
  justify-content: flex-end;
  margin-top: auto;
}

@keyframes labSweep {
  0%,
  42% {
    transform: translateX(-72%);
  }
  72%,
  100% {
    transform: translateX(72%);
  }
}

@keyframes numberPulse {
  0%,
  100% {
    text-shadow: 0 0 0 transparent;
  }
  50% {
    text-shadow: 0 0 12px color-mix(in srgb, var(--app-green) 72%, transparent);
  }
}

.about-panel {
  display: grid;
  grid-template-columns: 64px minmax(0, 1fr) auto;
  gap: 16px;
  align-items: center;
  padding: 20px 16px 0;
  border-top: 1px solid var(--app-border);
}

.about-avatar {
  width: 64px;
  height: 64px;
  overflow: hidden;
  border-radius: 16px;
  background: var(--app-surface-sunken);
}

.about-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-copy {
  display: grid;
  gap: 6px;
}

.about-copy h2 {
  font-size: 20px;
}

@media (max-width: 1080px) {
  .hero-section {
    grid-template-columns: 1fr;
  }

  .hero-section {
    min-height: 0;
    padding-bottom: 58px;
  }

  .section-heading--lab {
    position: static;
  }

  .ide-body,
  .ide-canvas {
    grid-template-columns: 1fr;
  }

  .ide-body {
    height: auto;
    min-height: 0;
  }

  .demo-rail {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    max-height: 260px;
    border-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .featured-reading {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 840px) {
  .home-main {
    width: min(100%, calc(100% - 24px));
    padding-top: 78px;
  }

  .section-heading {
    flex-direction: row;
  }

  .section-heading-side {
    justify-items: start;
  }

  .demo-lab-section {
    padding: 22px;
  }

  .demo-rail {
    grid-template-columns: 1fr;
  }

  .article-row,
  .about-panel {
    grid-template-columns: 1fr;
  }

  .featured-reading {
    grid-template-columns: 1fr;
    padding: 8px 16px;
  }

  .article-cover {
    max-width: none;
  }

  .ide-canvas {
    gap: 12px;
    padding: 12px;
  }

  .ide-editor {
    height: 360px;
  }

  .ide-preview {
    height: 320px;
  }

  .ide-tabs {
    overflow-x: auto;
  }

  .ide-statusbar {
    flex-wrap: wrap;
    gap: 8px 14px;
    padding: 8px 12px;
  }

  .about-panel {
    align-items: start;
  }
}

@media (max-width: 640px) {
  .home-main {
    width: min(100%, calc(100% - 16px));
    padding-bottom: 40px;
  }

  .hero-section {
    gap: 34px;
    padding-top: 4px;
    padding-bottom: 48px;
  }

  .hero-title {
    font-size: 34px;
  }

  .hero-title__pill {
    border-radius: 12px;
    box-shadow: 4px 4px 0 color-mix(in srgb, var(--accent) 24%, transparent);
  }

  .hero-subtitle,
  .hero-description {
    font-size: 16px;
  }

  .hero-index,
  .demo-lab-section {
    border-radius: 16px;
  }

  .index-card {
    min-height: 0;
  }
}
</style>
