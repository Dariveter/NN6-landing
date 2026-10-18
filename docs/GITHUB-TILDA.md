# Публикация: GitHub → GitHub Pages → Тильда

Схема: код лежит в GitHub, при каждом пуше в `main` GitHub Actions проверяет сайт (`npm test`), собирает `dist/` и публикует его на GitHub Pages. На Тильде страница `ne-institute.com/aicamp6-1` показывает этот сайт во весь экран через блок T123 с iframe. Править на Тильде ничего не нужно: пуш в GitHub — и через 1–2 минуты обновлённая версия уже на странице.

## Один раз: создать репозиторий

1. На github.com под аккаунтом **Dariveter** создайте репозиторий `NN6-landing` (**Public** — на бесплатном тарифе GitHub Pages работает только для публичных репозиториев; в проекте нет ключей и паролей, но в `history/` лежат старые рабочие материалы — если не хотите их публиковать, удалите папку `history/` перед первым пушем или оставьте её только в архиве).
2. Залейте проект. Через терминал из папки проекта:

```bash
git init -b main
git add .
git commit -m "FIELD winter landing, сверено с КП B2C"
git remote add origin https://github.com/Dariveter/NN6-landing.git
git push -u origin main
```

   Без терминала: GitHub Desktop → Add existing repository → папка проекта → Publish repository (снимите галочку «Keep this code private»).
3. В репозитории: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Откройте вкладку **Actions** и дождитесь зелёной галочки у «Deploy to GitHub Pages». Сайт появится по адресу **https://dariveter.github.io/NN6-landing/**.

## Один раз: Тильда

1. Создайте страницу с адресом `aicamp6-1` в проекте ne-institute.com.
2. В настройках страницы отключите шапку и подвал проекта (Настройки страницы → Ещё → «Не показывать header/footer»).
3. Добавьте блок **T123 (HTML-код)** и вставьте содержимое файла `tilda/t123/index.html`:

```html
<iframe src="https://dariveter.github.io/NN6-landing/index.html" title="Зимний интенсив НИИ Нейросетей" style="display:block;width:100%;height:100vh;height:100dvh;border:0" loading="eager" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
```

4. В настройках страницы впишите заголовок и описание для поисковиков и соцсетей (iframe их не передаёт) и опубликуйте.

Оплата идёт через корзину Тильды: рубли — `https://pay.ne-institute.com/aicamp6-1#order:Кэмп НН6=28000`, евро (Allpay в корзине) — `https://ne-institute.com/aicamp6-1#order:Кэмп НН6=280`. На странице `aicamp6-1` должен стоять блок корзины, а товар называться `Кэмп НН6`.

## Как вносить правки дальше

Правьте файлы в `site/`, затем пуш в `main` (или кнопка **Commit** в GitHub Desktop / редактирование файла прямо на github.com). Если проверка Нейрония упадёт, Actions покажет красный крестик и старая версия останется на месте.

## Ограничения iframe

- Поисковики индексируют страницу GitHub Pages, а не текст на ne-institute.com. Для рекламного лендинга это обычно не критично.
- Если позже понадобится отказаться от iframe, в `tilda/zero-block/` лежит полный HTML со встроенными стилями (`npm run tilda`), картинки в нём берутся с GitHub Pages.

Атрибуты `allow` и `allowfullscreen` в iframe нужны, чтобы видеоотзывы открывались во всплывающем окне и разворачивались на весь экран.
