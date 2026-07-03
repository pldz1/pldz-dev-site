<template>
  <MobileDrawer v-model="isMobileMenuOpen" subtitle="项目、教程、仓库和 Live Demo">
    <p>欢迎来到「爬楼的猪 Dev」</p>
    <p>这里放项目、教程、仓库、Live Demo 和一些零散记录。</p>
  </MobileDrawer>

  <HeaderBar :route-name="'首页'" :scroll="true" @toggle-mobile-menu="onToggleMobileMenu" />

  <div class="home-page">
    <div class="interaction-glow" :style="glowStyle" aria-hidden="true"></div>
    <main class="home-main">
      <section class="hero-section" aria-labelledby="home-title">
        <div class="hero-copy">
          <p class="hero-eyebrow">DEV SPACE</p>
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

          <ul class="hero-points">
            <li>开发里的零散内容，慢慢放到这里</li>
            <li>能复用的、能跑的、顺手能查的，会优先留下来</li>
          </ul>
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
            <h2 id="demo-lab-title">能上手玩的</h2>
          </div>
          <div class="section-heading-side">
            <p class="section-intro">一些点开就能看、能上手试的小东西。</p>
            <a class="section-link" href="/livedemo">全部 Demo<span class="link-arrow" aria-hidden="true"></span></a>
          </div>
        </div>

        <div class="demo-workbench">
          <div class="demo-rail" aria-label="Demo 列表">
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
                <span>{{ demo.description }}</span>
              </span>
              <span :class="['demo-tab__status', `demo-tab__status--${demo.status}`]">{{ demo.status === "done" ? "在线可用" : "看看" }}</span>
            </button>
          </div>

          <div class="lab-stage">
            <div class="code-panel" aria-label="Demo 元信息">
              <div class="panel-topbar">
                <span></span>
                <span></span>
                <span></span>
                <strong>demo.config</strong>
              </div>
              <pre><code><span v-for="line in selectedDemoCode" :key="line.id" :class="line.className">{{ line.text }}</span></code></pre>
            </div>

            <article class="result-panel" :key="selectedDemo.id || selectedDemo.title">
              <div class="result-preview">
                <img v-if="selectedDemo.thumbnail || selectedDemo.previewgif" :src="selectedDemo.thumbnail || selectedDemo.previewgif" :alt="selectedDemo.title" />
                <div v-else class="result-placeholder" aria-hidden="true">{{ demoInitials }}</div>
              </div>
              <div class="result-copy">
                <div class="result-meta">
                  <span>Result</span>
                  <span>{{ selectedDemo.status === "done" ? "已完成" : selectedDemo.status }}</span>
                </div>
                <h3>{{ selectedDemo.title || "未命名 Demo" }}</h3>
                <p>{{ selectedDemo.description || "暂无描述" }}</p>
                <div class="result-actions">
                  <a
                    class="button-primary button-small"
                    :href="selectedDemo.demoLink"
                    target="_blank"
                    rel="noopener noreferrer"
                    data-analytics-cta="live_demo"
                    :data-analytics-source="`home.demo_lab.${selectedDemo.id || selectedDemo.title || 'unknown'}`"
                    :data-analytics-label="selectedDemo.title || '在线体验'"
                  >
                    在线打开
                  </a>
                  <a class="button-ghost button-small" :href="selectedDemo.repoLink" target="_blank" rel="noopener noreferrer">GitHub</a>
                </div>
              </div>
            </article>
          </div>
        </div>

        <div ref="bridgeRef" class="code-product-story" :style="bridgeStyle" aria-labelledby="code-product-title">
        <div class="morph-copy">
          <p class="scene-no">03 / CODE → PRODUCT</p>
          <h2 id="code-product-title">代码整理成可读内容</h2>
          <p>这里不是单独展示一个窗口，而是把 Demo 的可运行信息、文章标题、摘要、分类和更新时间一起整理成下面的阅读系统。</p>
          <div class="morph-meter" aria-hidden="true">
            <span>Scene progress</span>
            <i><b></b></i>
          </div>
        </div>

        <div class="morph-visual" aria-label="代码转化为内容的视觉过渡">
          <div class="morph-code-window">
            <div class="morph-window-bar">
              <i></i>
              <i></i>
              <i></i>
              <strong>publish.pipeline</strong>
            </div>
            <div class="morph-code-lines">
              <span class="morph-line morph-line--muted">const demo = selectedDemo;</span>
              <span class="morph-line morph-line--accent">collect(demo.title, demo.demoLink);</span>
              <span class="morph-line">mapArticles([</span>
              <span v-for="article in morphArticles" :key="`code-${article.id}`" class="morph-line">  "{{ article.title }}",</span>
              <span class="morph-line">]);</span>
              <span class="morph-line morph-line--muted">sortBy(date).slice(0, updates.length);</span>
              <span class="morph-line morph-line--accent">return readingSurface;</span>
            </div>
          </div>

          <article class="morph-product-window">
            <div class="morph-window-bar morph-window-bar--light">
              <i></i>
              <i></i>
              <i></i>
              <strong>Blog</strong>
            </div>
            <div class="morph-product-body">
              <div class="morph-product-nav">
                <span>阅读入口</span>
                <a :href="featuredArticle.tutorialLink || '/articles'">看教程<span class="link-arrow" aria-hidden="true"></span></a>
              </div>
              <div class="morph-article-card morph-article-card--lead">
                <div class="morph-article-cover">
                  <img v-if="featuredArticle.cover" :src="featuredArticle.cover" :alt="featuredArticle.title" loading="lazy" decoding="async" />
                </div>
                <div class="morph-article-copy">
                  <div class="article-meta">
                    <span>{{ featuredArticle.category || featuredArticle.tags?.[0] || "文章" }}</span>
                    <span v-if="featuredArticle.date">{{ featuredArticle.date }}</span>
                  </div>
                  <h3>{{ featuredArticle.title || "未命名文章" }}</h3>
                  <p>{{ featuredArticle.description || "暂无描述" }}</p>
                  <div class="tag-list">
                    <span v-for="tag in featuredArticle.tags || []" :key="tag" class="tag-chip">{{ tag }}</span>
                  </div>
                </div>
              </div>

              <div class="morph-content-stack">
                <a v-for="(article, index) in morphArticles.slice(1)" :key="article.id" class="morph-mini-article" :href="article.tutorialLink" :style="getMorphItemStyle(index)">
                  <span>{{ article.category || article.tags?.[0] || "文章" }}</span>
                  <strong>{{ article.title }}</strong>
                  <small v-if="article.date">{{ article.date }}</small>
                </a>
              </div>

              <div class="morph-update-strip" aria-label="最近更新预览">
                <span v-for="item in morphUpdates" :key="`strip-${item.id}`">{{ formatDisplayDate(item.date) }} · {{ item.type }}</span>
              </div>
            </div>
          </article>

          <div class="float-token" aria-hidden="true">&lt;ReadingSurface /&gt;</div>
        </div>
        </div>
      </section>

      <section class="blog-section" aria-labelledby="blog-title">
        <div class="section-heading">
          <div>
            <p class="section-kicker">Blog</p>
            <h2 id="blog-title">最近写的</h2>
          </div>
          <div class="section-heading-side">
            <p class="section-intro">项目过程、配置折腾、工具记录，偶尔也有点偏实验的东西。</p>
            <a class="section-link" href="/articles">全部文章<span class="link-arrow" aria-hidden="true"></span></a>
          </div>
        </div>

        <div class="reading-layout">
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

          <aside class="updates-panel" aria-labelledby="updates-title">
            <div class="updates-heading">
              <div>
                <span class="updates-kicker">Activity</span>
                <h2 id="updates-title">最近更新</h2>
              </div>
              <a class="section-link section-link--light" href="/articles">看全部<span class="link-arrow" aria-hidden="true"></span></a>
            </div>
            <ul class="activity-list">
              <li v-for="(item, index) in updates" :key="item.id" class="activity-item" :style="getActivityStyle(index)">
                <a :href="item.link" class="activity-link">
                  <span class="activity-node" aria-hidden="true"></span>
                  <span class="activity-type">{{ item.type }}</span>
                  <strong>{{ item.title }}</strong>
                  <time v-if="item.date">{{ formatDisplayDate(item.date) }}</time>
                  <span class="activity-action">查看</span>
                </a>
              </li>
            </ul>
          </aside>
        </div>
      </section>

      <section class="about-panel">
        <div class="about-avatar">
          <img :src="'/api/v1/website/image/avatar/admin.jpg'" alt="about avatar" />
        </div>
        <div class="about-copy">
          <h2>关于我</h2>
          <p>平时写点项目、工具脚本、页面小实验和部署笔记。没什么严格边界，想到什么就慢慢补进来。</p>
        </div>
        <a class="button-ghost button-small" :href="githubLink">了解更多<span class="link-arrow" aria-hidden="true"></span></a>
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
const bridgeRef = ref(null);
const bridgeProgress = ref(0);
const pointerX = ref(0);
const pointerY = ref(0);

const series = ref([]);
const hotArticles = ref([]);
const demos = ref([]);
const updates = ref([]);

const githubLink = "https://github.com/pldz1";

const featuredSeries = computed(() => series.value[0] || {});
const secondarySeries = computed(() => series.value[1] || {});
const featuredDemo = computed(() => demos.value[0] || {});
const featuredArticle = computed(() => hotArticles.value[0] || {});
const morphArticles = computed(() => {
  const articles = hotArticles.value.length ? hotArticles.value : series.value;
  return articles.slice(0, 3);
});
const morphUpdates = computed(() => updates.value.slice(0, 3));
const selectedDemo = computed(() => demos.value[activeDemoIndex.value] || featuredDemo.value || {});

const selectedDemoCode = computed(() => {
  const demo = selectedDemo.value || {};
  return [
    { id: "open", className: "code-line code-line--muted", text: "export default {" },
    { id: "title", className: "code-line", text: `  title: "${escapeCodeText(demo.title || "未命名 Demo")}",` },
    { id: "status", className: "code-line", text: `  status: "${demo.status || "done"}",` },
    { id: "demo", className: "code-line code-line--accent", text: `  demoLink: "${escapeCodeText(demo.demoLink || "")}",` },
    { id: "repo", className: "code-line", text: `  repoLink: "${escapeCodeText(demo.repoLink || "")}",` },
    { id: "description", className: "code-line", text: `  description: "${escapeCodeText(demo.description || "暂无描述")}"` },
    { id: "close", className: "code-line code-line--muted", text: "}" },
  ];
});

const demoInitials = computed(() => String(selectedDemo.value?.title || "Demo").slice(0, 2).toUpperCase());

const bridgeStyle = computed(() => ({
  "--bridge-progress": bridgeProgress.value.toFixed(3),
  "--bridge-rest": (1 - bridgeProgress.value).toFixed(3),
  "--code-x": `${bridgeProgress.value * 120}px`,
  "--code-scale": (1 - bridgeProgress.value * 0.16).toFixed(3),
  "--code-rotate": `${bridgeProgress.value * 12}deg`,
  "--code-opacity": (1 - bridgeProgress.value * 0.44).toFixed(3),
  "--product-x": `${(1 - bridgeProgress.value) * -160}px`,
  "--product-scale": (0.82 + bridgeProgress.value * 0.18).toFixed(3),
  "--product-rotate": `${(1 - bridgeProgress.value) * -10}deg`,
  "--product-opacity": (0.26 + bridgeProgress.value * 0.74).toFixed(3),
  "--frame-opacity": (0.18 + bridgeProgress.value * 0.26).toFixed(3),
  "--meter-width": `${bridgeProgress.value * 100}%`,
  "--line-opacity": (0.3 + (1 - bridgeProgress.value) * 0.7).toFixed(3),
  "--line-x": `${bridgeProgress.value * 28}px`,
  "--beam-opacity": (0.14 + bridgeProgress.value * 0.72).toFixed(3),
  "--beam-scale": (0.4 + bridgeProgress.value * 0.8).toFixed(3),
  "--token-top": `${26 + bridgeProgress.value * 18}%`,
  "--token-left": `${40 + bridgeProgress.value * 12}%`,
  "--token-x": `${(1 - bridgeProgress.value) * 78}px`,
  "--token-rotate": `${(bridgeProgress.value - 0.5) * 12}deg`,
  "--token-opacity": (0.38 + bridgeProgress.value * 0.62).toFixed(3),
  "--lead-shine-x": `${-100 + bridgeProgress.value * 220}%`,
}));

const glowStyle = computed(() => ({
  "--mx": `${pointerX.value}px`,
  "--my": `${pointerY.value}px`,
}));

function escapeCodeText(value) {
  return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function formatNumber(value) {
  return String(value).padStart(2, "0");
}

function setActiveDemo(index) {
  activeDemoIndex.value = index;
}

function formatDisplayDate(date) {
  return String(date || "").replaceAll("-", ".");
}

function getMorphItemStyle(index) {
  const progress = bridgeProgress.value;
  return {
    "--stack-y": `${(1 - progress) * (18 + index * 10)}px`,
    "--stack-opacity": (0.38 + progress * 0.62 - index * 0.08).toFixed(3),
  };
}

function getActivityStyle(index) {
  return {
    "--activity-delay": `${index * 80}ms`,
  };
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

function normalizeUpdate(article, index) {
  return {
    id: article?.id || `update-${index}`,
    title: article?.title || "未命名文章",
    date: article?.date || "",
    type: article?.category || "article",
    link: article?.id ? `/article/${article.id}` : "/",
  };
}

async function loadHomeData() {
  const [articlesRes, articleIntrosRes, livedemoRes] = await Promise.allSettled([getAllArticles(), getArticleIntros(), getAllLiveDemos()]);

  const articles = articlesRes.status === "fulfilled" && Array.isArray(articlesRes.value) ? articlesRes.value : [];
  const articleIntros = articleIntrosRes.status === "fulfilled" && Array.isArray(articleIntrosRes.value) ? articleIntrosRes.value : [];
  const livedemos = livedemoRes.status === "fulfilled" && Array.isArray(livedemoRes.value) ? livedemoRes.value : [];

  const sortedArticles = [...articles].sort((a, b) => String(b?.date || "").localeCompare(String(a?.date || "")));
  const sortedSeries = [...articleIntros].sort((a, b) => String(b?.date || "").localeCompare(String(a?.date || "")));

  const seriesCards = sortedSeries
    .filter((article) => article?.category || article?.title)
    .slice(0, 3)
    .map(normalizeSeriesCard);

  const hotArticleCards = [...articles]
    .filter((article) => article?.id && article?.title)
    .sort((a, b) => (b?.views || 0) - (a?.views || 0) || String(b?.date || "").localeCompare(String(a?.date || "")))
    .slice(0, 3)
    .map(normalizeHotArticle);

  const updateArticles = sortedArticles
    .filter((article) => article?.id && article?.title)
    .slice(0, 5)
    .map(normalizeUpdate);

  const demoCards = livedemos.slice(0, 4).map(normalizeLiveDemo);

  series.value = seriesCards.length ? seriesCards : [];
  hotArticles.value = hotArticleCards.length ? hotArticleCards : [];
  updates.value = updateArticles.length ? updateArticles : [];
  demos.value = demoCards.length ? demoCards : [];
  activeDemoIndex.value = 0;
}

function updateBridgeProgress() {
  const bridge = bridgeRef.value;
  if (!bridge) return;

  const rect = bridge.getBoundingClientRect();
  const viewport = window.innerHeight || 1;
  const rawProgress = (viewport * 0.82 - rect.top) / (viewport * 0.7 + rect.height * 0.35);
  bridgeProgress.value = Math.min(1, Math.max(0, rawProgress));
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
  updateBridgeProgress();
}

function onPointerMove(event) {
  pointerX.value = event.clientX;
  pointerY.value = event.clientY;
}

onMounted(() => {
  pointerX.value = window.innerWidth * 0.64;
  pointerY.value = window.innerHeight * 0.36;
  window.addEventListener("resize", onResize);
  window.addEventListener("scroll", updateBridgeProgress, { passive: true });
  window.addEventListener("pointermove", onPointerMove, { passive: true });
  loadHomeData();
  updateBridgeProgress();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize);
  window.removeEventListener("scroll", updateBridgeProgress);
  window.removeEventListener("pointermove", onPointerMove);
});
</script>

<style scoped>
:global(body) {
  background:
    radial-gradient(circle at top left, color-mix(in srgb, var(--accent) 8%, transparent), transparent 34rem),
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
  background:
    radial-gradient(circle, color-mix(in srgb, var(--accent) 13%, transparent), color-mix(in srgb, var(--app-green) 5%, transparent) 42%, transparent 70%);
  filter: blur(18px);
  opacity: 0.72;
  pointer-events: none;
  transition: left 120ms var(--app-ease), top 120ms var(--app-ease);
}

.home-main {
  position: relative;
  z-index: 1;
  width: min(1240px, calc(100% - 40px));
  margin: 0 auto;
  padding: 58px 0 56px;
}

.hero-section {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(340px, 0.46fr);
  gap: 30px;
  align-items: end;
  min-height: 0;
  padding: 18px 0 28px;
}

.hero-copy {
  min-width: 0;
}

.hero-eyebrow,
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
  font-size: clamp(32px, 3.7vw, 48px);
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
  margin: 18px 0 0;
  color: color-mix(in srgb, var(--accent) 72%, var(--app-text));
  font-size: 18px;
  font-weight: 650;
  line-height: 1.5;
}

.hero-description {
  max-width: 620px;
  margin: 14px 0 0;
  color: var(--app-text-muted);
  font-size: 16px;
  line-height: 1.78;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}

.hero-button {
  height: 44px;
  padding: 0 18px;
}

.hero-points {
  display: grid;
  gap: 12px;
  max-width: 580px;
  margin: 20px 0 0;
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
  gap: 28px;
  margin-bottom: 24px;
}

.section-heading h2,
.updates-heading h2,
.about-copy h2 {
  margin: 0;
  color: var(--app-text);
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 1.2;
}

.section-heading h2 {
  font-size: 34px;
  letter-spacing: -0.02em;
}

.section-heading-side {
  display: grid;
  justify-items: end;
  gap: 10px;
}

.section-intro {
  max-width: 540px;
  margin: 0;
  color: var(--app-text-muted);
  font-size: 15px;
  line-height: 1.75;
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
  margin: 0 0 56px;
  padding: 30px;
  border: 1px solid color-mix(in srgb, var(--accent) 28%, var(--app-border));
  border-radius: 22px;
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--accent) 7%, transparent), transparent 210px),
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
  margin: 0 0 24px;
  padding: 0;
  background: transparent;
}

.demo-workbench {
  display: grid;
  grid-template-columns: minmax(280px, 0.34fr) minmax(0, 1fr);
  gap: 20px;
  align-items: stretch;
}

.demo-rail {
  display: grid;
  align-content: start;
  gap: 10px;
  min-width: 0;
}

.demo-tab {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 14px;
  width: 100%;
  min-height: 112px;
  padding: 15px 16px;
  border: 1px solid var(--app-border);
  border-radius: 14px;
  background: var(--app-surface);
  color: var(--app-text);
  text-align: left;
  cursor: pointer;
  box-shadow: none;
}

.demo-tab:hover,
.demo-tab--active {
  border-color: color-mix(in srgb, var(--app-text) 82%, var(--app-border));
  background: color-mix(in srgb, var(--app-green) 6%, var(--app-surface));
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--app-text) 76%, transparent);
  transform: none;
}

.demo-tab--active .demo-tab__number {
  animation: numberPulse 1.45s ease-in-out infinite;
}

.demo-tab__number {
  color: var(--app-green);
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 800;
}

.demo-tab__copy {
  display: grid;
  min-width: 0;
  gap: 7px;
}

.demo-tab__copy strong {
  overflow: hidden;
  color: var(--app-text);
  font-size: 16px;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.demo-tab__copy span {
  display: -webkit-box;
  overflow: hidden;
  color: var(--app-text-muted);
  font-size: 13px;
  line-height: 1.55;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.demo-tab__status {
  grid-column: 2;
  justify-self: start;
  padding: 5px 10px;
  border: 1px solid color-mix(in srgb, var(--app-green) 30%, transparent);
  border-radius: 999px;
  color: var(--app-green);
  font-size: 12px;
}

.lab-stage {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.04fr) minmax(280px, 0.8fr);
  gap: 20px;
  align-items: stretch;
  min-width: 0;
}

.lab-stage::before {
  content: "";
  position: absolute;
  z-index: 3;
  top: 48%;
  left: calc(52% - 46px);
  width: 92px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #70e8ff, var(--app-green), transparent);
  box-shadow: 0 0 18px color-mix(in srgb, var(--app-green) 58%, transparent);
  transform: translateX(-50%);
  animation: dataFlow 1.8s ease-in-out infinite;
  pointer-events: none;
}

.code-panel,
.result-panel {
  min-width: 0;
  overflow: hidden;
  border: 1px solid var(--app-border);
  border-radius: 18px;
  background: var(--app-surface);
  box-shadow: var(--app-shadow-sm);
}

.code-panel {
  position: relative;
  background: #111827;
  color: #d9e7ff;
  min-height: 410px;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.16);
}

.code-panel::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 54px;
  height: 80px;
  background: linear-gradient(180deg, transparent, rgba(112, 232, 255, 0.1), transparent);
  transform: translateY(-100%);
  animation: codeScan 4.6s ease-in-out infinite;
  pointer-events: none;
}

.panel-topbar {
  display: flex;
  align-items: center;
  gap: 7px;
  min-height: 46px;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.panel-topbar span {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: #ff6b6b;
}

.panel-topbar span:nth-child(2) {
  background: #ffd166;
}

.panel-topbar span:nth-child(3) {
  background: #63d297;
}

.panel-topbar strong {
  margin-left: auto;
  color: rgba(255, 255, 255, 0.6);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
}

.code-panel pre {
  margin: 0;
  padding: 20px 20px;
  overflow: auto;
  max-width: 100%;
}

.code-panel code {
  display: grid;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.58;
  white-space: pre;
}

.code-line {
  display: block;
}

.code-line--muted {
  color: rgba(217, 231, 255, 0.52);
}

.code-line--accent {
  color: #8dd7ff;
}

.result-panel {
  display: grid;
  grid-template-rows: 210px auto;
  min-height: 410px;
  animation: resultIn 220ms var(--app-ease);
}

.result-preview {
  position: relative;
  display: grid;
  min-height: 210px;
  overflow: hidden;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--app-green) 16%, transparent), transparent 52%),
    var(--app-surface-sunken);
  place-items: center;
}

.result-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.result-preview::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, transparent 20%, rgba(255, 255, 255, 0.26), transparent 48%);
  transform: translateX(-120%);
  animation: resultShine 3.8s ease-in-out infinite;
  pointer-events: none;
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

.result-copy {
  display: grid;
  gap: 12px;
  padding: 20px;
}

.result-meta,
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

.result-copy h3,
.article-copy h3 {
  margin: 0;
  color: var(--app-text);
  font-size: 21px;
  line-height: 1.35;
}

.result-copy p,
.article-copy p,
.about-copy p {
  margin: 0;
  color: var(--app-text-muted);
  line-height: 1.75;
}

.result-actions,
.article-bottom,
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.code-product-story {
  position: relative;
  display: grid;
  grid-template-columns: minmax(250px, 0.36fr) minmax(0, 1fr);
  gap: 30px;
  align-items: center;
  min-height: 470px;
  margin: 24px 0 0;
  padding: 28px;
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--app-green) 18%, var(--app-border));
  border-radius: 18px;
  background:
    radial-gradient(circle at 82% 50%, color-mix(in srgb, var(--accent) 9%, transparent), transparent 34%),
    linear-gradient(180deg, color-mix(in srgb, var(--app-surface) 76%, transparent), color-mix(in srgb, var(--app-bg) 76%, transparent));
  perspective: 1100px;
}

.code-product-story::after {
  content: "Demo output -> readable post";
  position: absolute;
  top: 14px;
  right: 18px;
  color: color-mix(in srgb, var(--app-text-soft) 72%, transparent);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.code-product-story::before {
  content: "";
  position: absolute;
  inset: 22px;
  border: 1px solid color-mix(in srgb, var(--app-border) 58%, transparent);
  border-radius: 18px;
  opacity: var(--frame-opacity);
  pointer-events: none;
}

.morph-copy {
  position: relative;
  z-index: 2;
  display: grid;
  gap: 16px;
  align-content: center;
  max-width: 360px;
}

.scene-no {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.scene-no::after {
  content: "";
  width: 62px;
  height: 1px;
  background: color-mix(in srgb, var(--accent) 42%, transparent);
}

.morph-copy h2 {
  margin: 0;
  color: var(--app-text);
  font-family: var(--font-display);
  font-size: clamp(28px, 3vw, 42px);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.02em;
}

.morph-copy p:not(.scene-no) {
  margin: 0;
  color: var(--app-text-muted);
  font-size: 15px;
  line-height: 1.75;
}

.morph-meter {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
  color: var(--app-text-soft);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.morph-meter i {
  display: block;
  width: 130px;
  height: 3px;
  overflow: hidden;
  border-radius: 999px;
  background: color-mix(in srgb, var(--app-border) 72%, transparent);
}

.morph-meter b {
  display: block;
  width: var(--meter-width);
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent), var(--app-green));
  box-shadow: 0 0 16px color-mix(in srgb, var(--app-green) 42%, transparent);
}

.morph-visual {
  position: relative;
  z-index: 1;
  min-height: 420px;
  transform-style: preserve-3d;
}

.morph-code-window,
.morph-product-window {
  position: absolute;
  top: 50%;
  width: min(520px, 58%);
  min-height: 326px;
  overflow: hidden;
  border-radius: 20px;
  box-shadow: 0 28px 70px rgba(15, 23, 42, 0.16);
  transform-style: preserve-3d;
  will-change: transform, opacity;
}

.morph-code-window {
  left: 0;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: #111827;
  color: #d9e7ff;
  opacity: var(--code-opacity);
  transform: translate3d(var(--code-x), -50%, 0) scale(var(--code-scale)) rotateY(var(--code-rotate));
}

.morph-product-window {
  right: 0;
  border: 1px solid var(--app-border);
  background: var(--app-surface);
  color: var(--app-text);
  opacity: var(--product-opacity);
  transform: translate3d(var(--product-x), -50%, 80px) scale(var(--product-scale)) rotateY(var(--product-rotate));
}

.morph-visual::before {
  content: "";
  position: absolute;
  z-index: 4;
  top: 50%;
  left: 44%;
  width: 176px;
  height: 3px;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, #70e8ff, var(--app-green), transparent);
  box-shadow: 0 0 22px color-mix(in srgb, var(--app-green) 58%, transparent);
  opacity: var(--beam-opacity);
  transform: translate(-50%, -50%) scaleX(var(--beam-scale));
  transform-origin: left;
  animation: morphBeam 1.8s ease-in-out infinite;
  pointer-events: none;
}

.morph-window-bar {
  display: flex;
  align-items: center;
  gap: 7px;
  height: 46px;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.morph-window-bar i {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: #ff6b6b;
}

.morph-window-bar i:nth-child(2) {
  background: #ffd166;
}

.morph-window-bar i:nth-child(3) {
  background: #63d297;
}

.morph-window-bar strong {
  margin-left: auto;
  color: rgba(255, 255, 255, 0.62);
  font-family: var(--font-mono);
  font-size: 12px;
}

.morph-window-bar--light {
  border-bottom-color: var(--app-border);
}

.morph-window-bar--light i {
  background: color-mix(in srgb, var(--app-text-soft) 42%, transparent);
}

.morph-window-bar--light strong {
  color: var(--app-text-soft);
}

.morph-code-lines {
  display: grid;
  gap: 9px;
  padding: 22px;
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.55;
}

.morph-line {
  display: block;
  opacity: var(--line-opacity);
  transform: translateX(var(--line-x));
}

.morph-line--muted {
  color: rgba(217, 231, 255, 0.52);
}

.morph-line--accent {
  color: #8dd7ff;
}

.morph-product-body {
  display: grid;
  gap: 14px;
  padding: 18px;
}

.morph-product-nav {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.morph-product-nav span {
  color: var(--app-text);
  font-size: 18px;
  font-weight: 800;
}

.morph-product-nav a {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--accent);
  font-size: 13px;
  font-weight: 800;
  text-decoration: none;
}

.morph-article-card {
  display: grid;
  grid-template-columns: 148px minmax(0, 1fr);
  gap: 16px;
  padding: 14px;
  border: 1px solid var(--app-border);
  border-radius: 16px;
  background: color-mix(in srgb, var(--app-bg) 52%, var(--app-surface));
}

.morph-article-card--lead {
  position: relative;
  overflow: hidden;
}

.morph-article-card--lead::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, transparent 28%, color-mix(in srgb, var(--accent) 10%, transparent), transparent 54%);
  transform: translateX(var(--lead-shine-x));
  opacity: 0.58;
  pointer-events: none;
}

.morph-article-cover {
  overflow: hidden;
  aspect-ratio: 16 / 11;
  border-radius: 12px;
  background: var(--app-surface-sunken);
}

.morph-article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.morph-article-copy {
  display: grid;
  gap: 8px;
  min-width: 0;
}

.morph-article-copy h3 {
  margin: 0;
  color: var(--app-text);
  font-size: 19px;
  line-height: 1.35;
}

.morph-article-copy p {
  display: -webkit-box;
  margin: 0;
  overflow: hidden;
  color: var(--app-text-muted);
  font-size: 14px;
  line-height: 1.65;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.morph-content-stack {
  display: grid;
  gap: 8px;
}

.morph-mini-article {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  min-height: 42px;
  padding: 9px 12px;
  border: 1px solid var(--app-border);
  border-radius: 12px;
  background: var(--app-surface);
  color: inherit;
  text-decoration: none;
  opacity: var(--stack-opacity);
  transform: translateY(var(--stack-y));
}

.morph-mini-article span {
  padding: 4px 8px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--accent) 9%, transparent);
  color: var(--accent);
  font-size: 12px;
  white-space: nowrap;
}

.morph-mini-article strong {
  overflow: hidden;
  color: var(--app-text);
  font-size: 14px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.morph-mini-article small {
  color: var(--app-text-soft);
  font-size: 12px;
  white-space: nowrap;
}

.morph-update-strip {
  display: flex;
  gap: 8px;
  overflow: hidden;
  mask-image: linear-gradient(90deg, #000 78%, transparent);
}

.morph-update-strip span {
  flex: 0 0 auto;
  padding: 5px 9px;
  border: 1px solid var(--app-border);
  border-radius: 999px;
  background: color-mix(in srgb, var(--app-bg) 58%, var(--app-surface));
  color: var(--app-text-muted);
  font-size: 12px;
}

.float-token {
  position: absolute;
  z-index: 5;
  top: var(--token-top);
  left: var(--token-left);
  padding: 10px 12px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 10px;
  background: #111827;
  color: #8dd7ff;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 800;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.22);
  transform: translateX(var(--token-x)) rotate(var(--token-rotate));
  opacity: var(--token-opacity);
}

.blog-section {
  margin-bottom: 56px;
}

.reading-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(318px, 0.36fr);
  gap: 30px;
  align-items: start;
}

.featured-reading {
  display: grid;
  border-top: 1px solid var(--app-border);
}

.article-row {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 24px;
  padding: 24px 0;
  border-bottom: 1px solid var(--app-border);
}

.article-cover {
  display: block;
  overflow: hidden;
  aspect-ratio: 16 / 10;
  border: 1px solid var(--app-border);
  border-radius: 14px;
  background: var(--app-surface-sunken);
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 220ms var(--app-ease);
}

.article-row:hover .article-cover img {
  transform: scale(1.035);
}

.article-copy {
  display: grid;
  min-width: 0;
  gap: 12px;
  align-content: start;
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
  -webkit-line-clamp: 2;
  font-size: 15px;
}

.article-bottom {
  justify-content: space-between;
  margin-top: 4px;
}

.updates-panel {
  position: sticky;
  top: 92px;
  overflow: hidden;
  padding: 22px 22px 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  background:
    radial-gradient(circle at 100% 0%, rgba(112, 232, 255, 0.1), transparent 34%),
    linear-gradient(180deg, #121826, #0f1724);
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.16);
}

.updates-panel::before {
  content: "";
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(180deg, transparent 0 28px, rgba(255, 255, 255, 0.035) 28px 29px);
  opacity: 0.55;
  pointer-events: none;
}

.updates-heading {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 16px;
  margin-bottom: 18px;
}

.updates-heading h2 {
  margin: 4px 0 0;
  color: #f8fbff;
  font-size: 24px;
}

.updates-kicker {
  color: #70e8ff;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.section-link--light {
  color: #70e8ff;
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

@keyframes dataFlow {
  0% {
    opacity: 0;
    transform: translateX(-66%) scaleX(0.45);
  }
  45% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateX(18%) scaleX(1);
  }
}

@keyframes codeScan {
  0%,
  38% {
    transform: translateY(-100%);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  78%,
  100% {
    transform: translateY(360px);
    opacity: 0;
  }
}

@keyframes resultShine {
  0%,
  52% {
    transform: translateX(-120%);
  }
  82%,
  100% {
    transform: translateX(120%);
  }
}

@keyframes resultIn {
  from {
    opacity: 0;
    transform: translateY(5px) scale(0.995);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes morphBeam {
  0% {
    filter: saturate(1);
    clip-path: inset(0 78% 0 0);
  }
  48% {
    filter: saturate(1.4);
    clip-path: inset(0 18% 0 0);
  }
  100% {
    filter: saturate(1);
    clip-path: inset(0 0 0 72%);
  }
}

@keyframes activityIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.activity-list {
  position: relative;
  z-index: 1;
  display: grid;
  margin: 0;
  padding: 0;
  list-style: none;
}

.activity-item + .activity-item {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.activity-link {
  position: relative;
  display: grid;
  grid-template-columns: 12px minmax(0, 1fr) auto;
  gap: 10px 12px;
  align-items: center;
  min-height: 74px;
  padding: 14px 0;
  color: inherit;
  text-decoration: none;
  animation: activityIn 520ms var(--app-ease) both;
  animation-delay: var(--activity-delay);
}

.activity-node {
  grid-row: 1 / span 3;
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: #70e8ff;
  box-shadow: 0 0 0 5px rgba(112, 232, 255, 0.12), 0 0 18px rgba(112, 232, 255, 0.38);
}

.activity-type {
  justify-self: start;
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(248, 251, 255, 0.72);
  font-size: 12px;
  line-height: 1;
}

.activity-link strong {
  grid-column: 2 / 4;
  color: #f8fbff;
  font-size: 15px;
  line-height: 1.5;
}

.activity-link time {
  color: rgba(248, 251, 255, 0.52);
  font-size: 13px;
}

.activity-action {
  justify-self: end;
  color: #70e8ff;
  font-size: 13px;
  font-weight: 800;
}

.activity-link:hover strong {
  color: #70e8ff;
}

.about-panel {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr) auto;
  gap: 18px;
  align-items: center;
  padding: 24px 0 0;
  border-top: 1px solid var(--app-border);
}

.about-avatar {
  width: 72px;
  height: 72px;
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
  font-size: 22px;
}

@media (max-width: 1080px) {
  .hero-section,
  .demo-workbench,
  .lab-stage,
  .code-product-story,
  .reading-layout {
    grid-template-columns: 1fr;
  }

  .lab-stage {
    grid-column: auto;
  }

  .hero-section {
    min-height: 0;
    padding-bottom: 58px;
  }

  .section-heading--lab,
  .updates-panel {
    position: static;
  }

  .demo-rail {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 840px) {
  .home-main {
    width: min(100%, calc(100% - 24px));
    padding-top: 94px;
  }

  .section-heading {
    align-items: start;
    flex-direction: column;
  }

  .section-heading-side {
    justify-items: start;
  }

  .demo-lab-section {
    padding: 22px;
  }

  .demo-rail,
  .article-row,
  .about-panel {
    grid-template-columns: 1fr;
  }

  .article-cover {
    max-width: 420px;
  }

  .code-product-story {
    min-height: 0;
    padding: 24px;
  }

  .morph-copy {
    max-width: none;
  }

  .morph-visual {
    min-height: 520px;
  }

  .morph-code-window,
  .morph-product-window {
    width: min(100%, 560px);
  }

  .morph-code-window {
    left: 0;
    top: 32%;
  }

  .morph-product-window {
    right: 0;
    top: 68%;
  }

  .morph-visual::before {
    top: 50%;
    left: 50%;
    width: 3px;
    height: 128px;
    transform: translate(-50%, -50%) scaleY(var(--beam-scale));
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
  .demo-lab-section,
  .updates-panel {
    border-radius: 16px;
  }

  .index-card {
    min-height: 0;
  }

  .code-product-story {
    margin: 18px 0 0;
    padding: 18px;
    border-radius: 16px;
  }

  .morph-visual {
    min-height: 560px;
  }

  .morph-code-window,
  .morph-product-window {
    min-height: 270px;
    border-radius: 16px;
  }

  .morph-code-lines {
    padding: 16px;
    font-size: 11px;
  }

  .morph-article-card {
    grid-template-columns: 1fr;
  }

  .morph-article-cover {
    max-height: 150px;
  }

  .article-bottom {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
