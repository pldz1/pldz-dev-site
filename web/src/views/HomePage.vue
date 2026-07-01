<template>
  <MobileDrawer v-model="isMobileMenuOpen" subtitle="项目、教程、仓库和 Live Demo">
    <p>欢迎来到「爬楼的猪 Dev」</p>
    <p>这里放项目、教程、仓库、Live Demo 和一些零散记录。</p>
  </MobileDrawer>

  <HeaderBar :route-name="'首页'" @toggle-mobile-menu="onToggleMobileMenu" />

  <div class="home-page">
    <main class="home-main">
      <section class="hero-section">
        <div class="hero-copy">
          <h1>随手做的小东西，<br />都丢在这儿了。</h1>
          <p class="hero-description">
            平时折腾的项目、写过的教程，还有能直接点开玩的小 demo。<br />
            都是自己一点点攒下来的，想到什么就往里加。
          </p>
          <div class="hero-actions">
            <a class="button-primary" href="/articles">看教程</a>
            <a
              class="button-ghost"
              href="/livedemo"
              data-analytics-cta="live_demo"
              data-analytics-source="home.hero"
              data-analytics-label="查看 Demo / GitHub"
            >
              翻翻 Demo
            </a>
          </div>
          <ul class="hero-points">
            <li>不太成体系，想到什么写什么</li>
            <li>能复用、能跑、回头查着方便的，会留下来</li>
          </ul>
        </div>

        <div class="hero-preview">
          <article class="preview-card preview-card--feature">
            <div class="preview-card__header">
              <span class="preview-card__eyebrow">最新教程</span>
              <span class="preview-status">还在写</span>
            </div>
            <h2>{{ featuredSeries.title }}</h2>
            <p class="preview-card__description">{{ featuredSeries.description }}</p>
            <div class="preview-tags">
              <span v-for="tag in featuredSeries.tags" :key="tag">{{ tag }}</span>
            </div>
            <a class="text-link" :href="featuredSeries.tutorialLink">去看看 →</a>
          </article>

          <div class="preview-grid">
            <article class="preview-card">
              <div class="preview-inline-meta">
                <span class="preview-card__eyebrow">在线 demo</span>
                <span class="preview-status preview-status--muted">{{ featuredDemo.status === "done" ? "可以打开" : "看看" }}</span>
              </div>
              <h3>{{ featuredDemo.title }}</h3>
              <p class="preview-card__description">{{ featuredDemo.description }}</p>
              <a
                class="text-link"
                :href="featuredDemo.demoLink"
                target="_blank"
                rel="noopener noreferrer"
                data-analytics-cta="live_demo"
                data-analytics-source="home.featured_demo"
                :data-analytics-label="featuredDemo.title || '在线体验'"
              >
                在线打开 →
              </a>
            </article>

            <article class="preview-card">
              <div class="preview-inline-meta">
                <span class="preview-card__eyebrow">还想看</span>
                <span class="preview-status preview-status--muted">{{ secondarySeries.tags?.[0] || "文章" }}</span>
              </div>
              <h3>{{ secondarySeries.title }}</h3>
              <p class="preview-card__description">{{ secondarySeries.description }}</p>
              <a class="text-link" :href="secondarySeries.tutorialLink">去读读 →</a>
            </article>
          </div>
        </div>
      </section>

      <section class="content-section">
        <div class="section-heading">
          <div>
            <h2>最近写的</h2>
          </div>
          <div class="section-heading-side">
            <p class="section-intro">项目过程、配置折腾、工具记录，偶尔也有点偏实验的东西。</p>
            <a class="section-link" href="/articles">全部文章 →</a>
          </div>
        </div>

        <div class="projects-grid">
          <ProjectCard v-for="article in hotArticles" :key="article.id" :project="article" />
        </div>
      </section>

      <section class="content-section demo-section">
        <div class="section-heading">
          <div>
            <h2>能上手玩的</h2>
          </div>
          <div class="section-heading-side">
            <p class="section-intro">一些点开就能看、能上手试的小东西。</p>
            <a class="section-link" href="/livedemo">全部 Demo →</a>
          </div>
        </div>

        <div class="demo-grid">
          <DemoCard v-for="demo in demos" :key="demo.id" :demo="demo" />
        </div>
      </section>

      <section class="content-section updates-and-about">
        <div class="updates-panel">
          <div class="section-heading section-heading--compact">
            <div>
              <h2>最近更新</h2>
            </div>
            <a class="section-link" href="/articles">看全部 →</a>
          </div>

          <ul class="updates-list">
            <TimelineItem v-for="item in updates" :key="item.id" :item="item" />
          </ul>
        </div>

        <section class="about-panel card-surface">
          <div class="about-avatar">
            <img :src="'/api/v1/website/image/avatar/admin.jpg'" alt="about avatar" />
          </div>
          <div class="about-copy">
            <h2>关于我</h2>
            <p>平时写点项目、工具脚本、页面小实验和部署笔记。没什么严格边界，想到什么就慢慢补进来。</p>
            <a class="button-ghost button-small" :href="githubLink">了解更多 →</a>
          </div>
        </section>
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
import DemoCard from "../components/home-page/DemoCard.vue";
import ProjectCard from "../components/home-page/ProjectCard.vue";
import TimelineItem from "../components/home-page/TimelineItem.vue";
import { getAllLiveDemos, getAllArticles, getArticleIntros } from "../utils/apis";

const isMobileMenuOpen = ref(false);

const series = ref([]);
const hotArticles = ref([]);
const demos = ref([]);
const updates = ref([]);

const githubLink = "https://github.com/pldz1";

const featuredSeries = computed(() => series.value[0] || {});
const secondarySeries = computed(() => series.value[1] || {});
const featuredDemo = computed(() => demos.value[0] || {});

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

  const democards = livedemos.slice(0, 4).map(normalizeLiveDemo);

  series.value = seriesCards.length ? seriesCards : [];
  hotArticles.value = hotArticleCards.length ? hotArticleCards : [];
  updates.value = updateArticles.length ? updateArticles : [];
  demos.value = democards.length ? democards : [];
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

onMounted(() => {
  window.addEventListener("resize", onResize);
  loadHomeData();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize);
});
</script>

<style scoped>
:global(body) {
  background: var(--app-bg);
  color: var(--app-text);
}

.home-page {
  min-height: 100vh;
}

.home-main {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 108px 0 56px;
}

.card-surface {
  background: var(--app-surface);
  border: 1px solid var(--app-border);
  border-radius: var(--app-radius-lg);
  box-shadow: var(--app-shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

.card-surface:hover {
  transform: translateY(-1px);
  box-shadow: var(--app-shadow-md);
  border-color: var(--app-border-strong);
  background: var(--app-surface);
}

.hero-copy.card-surface,
.about-panel.card-surface {
  background: transparent;
  border-color: transparent;
  box-shadow: none;
}

.hero-copy.card-surface:hover,
.about-panel.card-surface:hover {
  transform: none;
  box-shadow: none;
  border-color: transparent;
  background: transparent;
}

.hero-section {
  display: grid;
  grid-template-columns: minmax(0, 1.02fr) minmax(0, 0.98fr);
  gap: 24px;
  margin-bottom: 72px;
  align-items: start;
}

.hero-copy {
  padding: 28px 12px 28px 0;
}

.hero-copy h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(33px, 4.4vw, 48px);
  font-weight: 600;
  line-height: 1.14;
  letter-spacing: -0.01em;
  color: var(--app-text);
}

.hero-description {
  margin: 18px 0 0;
  font-size: 16px;
  line-height: 1.8;
  color: var(--app-text-muted);
}

.hero-actions,
.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.hero-actions {
  margin-top: 28px;
}

.hero-points {
  margin: 30px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 12px;
}

.hero-points li {
  position: relative;
  padding-left: 18px;
  color: var(--app-text-muted);
  line-height: 1.7;
}

.hero-points li::before {
  content: "";
  position: absolute;
  top: 10px;
  left: 0;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--app-blue);
}

.hero-preview {
  display: grid;
  gap: 18px;
}

.preview-card {
  padding: 24px;
  border: 1px solid var(--app-border);
  border-radius: var(--app-radius-lg);
  background: var(--app-surface);
  box-shadow: var(--app-shadow-sm);
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease, background-color 0.22s ease;
}

.preview-card--feature {
  padding: 30px 30px 28px;
}

.preview-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--app-shadow-md);
  border-color: var(--app-border-strong);
  background: var(--app-surface);
}

.preview-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.preview-card__eyebrow {
  font-size: 12px;
  color: var(--app-text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.preview-inline-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.preview-status {
  padding: 6px 10px;
  border-radius: 999px;
  background: var(--accent-weak);
  color: var(--app-blue);
  border: 1px solid var(--accent-line);
  font-size: 12px;
}

.preview-status--muted {
  background: var(--app-surface);
  color: var(--app-text-muted);
  border-color: var(--app-border);
}

.preview-card h2,
.preview-card h3,
.project-card h3,
.demo-card h3,
.about-copy h2,
.section-heading h2 {
  margin: 0;
  color: var(--app-text);
}

.preview-card h2 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 24px;
  line-height: 1.35;
}

.preview-card h3,
.project-card h3,
.demo-card h3 {
  font-size: 20px;
  line-height: 1.35;
}

.preview-grid .preview-card h3 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-card p,
.project-card p,
.demo-card p,
.about-copy p,
.section-intro {
  color: var(--app-text-muted);
  line-height: 1.75;
}

.preview-card__description {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.preview-tags,
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preview-tags {
  margin: 20px 0;
}

.preview-tags span,
.tag-chip {
  display: inline-flex;
  align-items: center;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid var(--app-border);
  background: var(--app-surface);
  color: var(--app-text-muted);
  font-size: 12px;
}

.preview-tags span {
  background: var(--app-surface);
  border-color: var(--app-border);
}

.tag-chip--muted {
  background: var(--app-surface);
}

.text-link {
  display: inline-flex;
  align-items: center;
  color: var(--app-blue);
  text-decoration: none;
  font-weight: 600;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.content-section {
  margin-bottom: 72px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 24px;
  margin-bottom: 28px;
}

.section-heading h2 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 28px;
  line-height: 1.2;
}

.section-intro {
  max-width: 520px;
  margin: 0;
  font-size: 15px;
}

.section-heading-side {
  display: grid;
  justify-items: end;
  gap: 10px;
}

.section-heading--compact {
  margin-bottom: 18px;
}

.section-link {
  color: var(--app-blue);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.about-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.demo-section {
  padding: 12px 0 0;
  border-radius: 0;
  background: transparent;
  border: none;
}

.demo-grid {
  display: grid;
  gap: 14px;
}

.updates-and-about {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.72fr);
  gap: 20px;
  align-items: start;
}

.updates-panel {
  padding: 0;
}

.about-panel {
  padding: 12px 0 0 24px;
  border-left: 1px solid var(--app-border);
  border-radius: 0;
}

.updates-panel,
.about-panel {
  align-self: start;
}

.updates-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  border-top: 1px solid var(--app-border);
}

.about-panel {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 18px;
}

.about-avatar {
  width: 88px;
  height: 88px;
  overflow: hidden;
  border-radius: var(--app-radius-lg);
  background: var(--app-surface-sunken);
}

.about-copy {
  display: grid;
  gap: 14px;
}

.about-copy h2 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 24px;
}

@media (max-width: 1080px) {
  .hero-section,
  .updates-and-about {
    grid-template-columns: 1fr;
  }

  .about-panel {
    grid-template-columns: 72px 1fr;
  }

  .about-avatar {
    width: 72px;
    height: 72px;
    border-radius: 20px;
  }
}

@media (max-width: 840px) {
  .home-main {
    width: min(100%, calc(100% - 24px));
    padding-top: 94px;
  }

  .hero-section,
  .projects-grid,
  .preview-grid {
    grid-template-columns: 1fr;
  }

  .section-heading {
    align-items: start;
    flex-direction: column;
  }

  .section-heading-side {
    justify-items: start;
  }
}

@media (max-width: 640px) {
  .home-main {
    width: min(100%, calc(100% - 16px));
    padding-bottom: 40px;
  }

  .hero-copy,
  .preview-card,
  .preview-card--feature,
  .about-panel {
    padding: 22px;
  }

  .hero-copy h1 {
    font-size: 30px;
  }

  .section-heading h2 {
    font-size: 24px;
  }

  .about-panel {
    grid-template-columns: 72px 1fr;
  }
}
</style>
