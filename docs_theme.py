"""Tema visual para /docs (Swagger UI), inspirado en las guías de diseño de Apple.

- Tipografía del sistema (SF Pro en Apple, Segoe UI en Windows) y mono del sistema para código.
- Claro y oscuro automáticos según el sistema (sin interruptor propio).
- Colores semánticos: cada método HTTP tiene su color Y su texto (nunca solo color).
- Movimiento mínimo y desactivado si el usuario pide "reducir movimiento".
"""
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

CSS = """
:root {
  --font: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI Variable Text", "Segoe UI", system-ui, Roboto, sans-serif;
  --mono: ui-monospace, "SF Mono", "Cascadia Code", Menlo, Consolas, monospace;
  --bg: #F5F5F7;  --card: #FFFFFF;  --fill: #F0F0F3;
  --label: #1D1D1F;  --secondary: #6E6E73;
  --sep: #D2D2D7;  --sep-strong: #B4B4BA;
  --link: #0066CC;  --btn: #0071E3;  --on-btn: #FFFFFF;  --danger: #C41E1E;
  --get-bg: #E6F0FC;  --get-fg: #0A5CC2;
  --post-bg: #E3F6E8; --post-fg: #1B7A35;
  --put-bg: #FFF1DC;  --put-fg: #8F4B00;
  --del-bg: #FDE6E6;  --del-fg: #B3141A;
  --code-bg: #1C1C1E;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #000000;  --card: #1C1C1E;  --fill: #2C2C2E;
    --label: #F5F5F7;  --secondary: #A1A1A6;
    --sep: #38383A;  --sep-strong: #545458;
    --link: #2997FF;  --danger: #FF6961;
    --get-bg: #0A2A4D;  --get-fg: #6CB4FF;
    --post-bg: #0F3320; --post-fg: #5FD47F;
    --put-bg: #3D2A08;  --put-fg: #FFB84D;
    --del-bg: #451515;  --del-fg: #FF8A80;
    --code-bg: #2C2C2E;
  }
}

html { color-scheme: light dark; }
body { margin: 0; background: var(--bg); -webkit-font-smoothing: antialiased; }
.swagger-ui .wrapper { max-width: 960px; padding: 0 24px 64px; }

/* ---------- Tipografía ---------- */
.swagger-ui *:not(pre):not(pre *):not(code) { font-family: var(--font); }
.swagger-ui pre, .swagger-ui pre *, .swagger-ui code,
.swagger-ui textarea, .swagger-ui .opblock .opblock-summary-path { font-family: var(--mono); }

/* ---------- Color de texto (semántico) ---------- */
.swagger-ui, .swagger-ui .info .title, .swagger-ui .info p, .swagger-ui .info li,
.swagger-ui .opblock-tag, .swagger-ui .opblock-summary-path, .swagger-ui label,
.swagger-ui .opblock .opblock-section-header h4, .swagger-ui .opblock .opblock-section-header label,
.swagger-ui .opblock-description-wrapper p, .swagger-ui .opblock-title_normal p,
.swagger-ui .responses-inner h4, .swagger-ui .responses-inner h5,
.swagger-ui table thead tr th, .swagger-ui table thead tr td,
.swagger-ui .parameter__name, .swagger-ui .parameter__type, .swagger-ui .parameter__in,
.swagger-ui .response-col_status, .swagger-ui .response-col_description,
.swagger-ui .tab li, .swagger-ui .markdown p, .swagger-ui .renderedMarkdown p,
.swagger-ui .model, .swagger-ui .model-title, .swagger-ui .prop-type { color: var(--label); }
.swagger-ui .opblock-summary-description, .swagger-ui .opblock-tag small,
.swagger-ui .parameter__type, .swagger-ui .parameter__in, .swagger-ui .prop-format,
.swagger-ui .tab li button.tablinks, .swagger-ui .response-col_links { color: var(--secondary); }
.swagger-ui .tab li.active button.tablinks { color: var(--label); }
.swagger-ui .parameter__name.required span,
.swagger-ui .parameter__name.required::after { color: var(--danger); }
.swagger-ui a { color: var(--link); }

/* ---------- Encabezado ---------- */
.swagger-ui .info { margin: 56px 0 28px; }
.swagger-ui .info .title { font-size: 40px; font-weight: 700; letter-spacing: -0.022em; line-height: 1.1; }
.swagger-ui .info .title small { background: var(--fill); color: var(--secondary); border-radius: 980px;
  padding: 3px 10px; font-size: 12px; font-weight: 600; top: -2px; }
.swagger-ui .info .title small pre { color: inherit; font-family: var(--font); }
.swagger-ui .info p { font-size: 17px; line-height: 1.47; color: var(--secondary); }
.swagger-ui .info a { font-size: 15px; }
.swagger-ui .scheme-container { background: transparent; box-shadow: none; padding: 0; }

/* Elemento firma: baliza de emergencia junto al título */
.swagger-ui .info .title::before {
  content: ""; display: inline-block; width: 12px; height: 12px; border-radius: 50%;
  background: var(--btn); margin-right: 14px; vertical-align: 0.12em;
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--btn) 25%, transparent);
}
@media (prefers-reduced-motion: no-preference) {
  .swagger-ui .info .title::before { animation: baliza 2.4s ease-out infinite; }
  @keyframes baliza {
    0%   { box-shadow: 0 0 0 0 color-mix(in srgb, var(--btn) 45%, transparent); }
    70%  { box-shadow: 0 0 0 10px transparent; }
    100% { box-shadow: 0 0 0 0 transparent; }
  }
  .swagger-ui .opblock-body { animation: abrir 0.16s ease-out; }
  @keyframes abrir { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
}

/* ---------- Grupos (tags) ---------- */
.swagger-ui .opblock-tag { font-size: 22px; font-weight: 600; letter-spacing: -0.01em;
  border-bottom: 1px solid var(--sep); padding: 22px 4px 12px; margin: 0 0 12px; }
.swagger-ui .opblock-tag small { font-size: 14px; font-weight: 400; }
.swagger-ui .opblock-tag:hover { background: transparent; }
.swagger-ui .opblock-tag svg, .swagger-ui .expand-operation svg { fill: var(--secondary); }

/* ---------- Operaciones como tarjetas ---------- */
.swagger-ui .opblock.opblock-get, .swagger-ui .opblock.opblock-post,
.swagger-ui .opblock.opblock-put, .swagger-ui .opblock.opblock-delete {
  background: var(--card); border: 1px solid var(--sep); border-radius: 14px;
  box-shadow: none; margin: 0 0 10px; overflow: hidden;
}
.swagger-ui .opblock .opblock-summary { border: 0; padding: 10px 14px; align-items: center; }
.swagger-ui .opblock.is-open .opblock-summary { border-bottom: 1px solid var(--sep); }
.swagger-ui .opblock .opblock-summary-path { font-size: 15px; font-weight: 500; }
.swagger-ui .opblock .opblock-summary-description { font-size: 14px; }
.swagger-ui .opblock .opblock-summary-method {
  min-width: 68px; padding: 6px 10px; border-radius: 980px; text-shadow: none;
  font-size: 12px; font-weight: 700; letter-spacing: 0.04em;
}
.swagger-ui .opblock.opblock-get .opblock-summary-method    { background: var(--get-bg);  color: var(--get-fg); }
.swagger-ui .opblock.opblock-post .opblock-summary-method   { background: var(--post-bg); color: var(--post-fg); }
.swagger-ui .opblock.opblock-put .opblock-summary-method    { background: var(--put-bg);  color: var(--put-fg); }
.swagger-ui .opblock.opblock-delete .opblock-summary-method { background: var(--del-bg);  color: var(--del-fg); }
.swagger-ui .opblock .opblock-section-header { background: var(--fill); box-shadow: none; padding: 10px 16px; }
.swagger-ui .opblock .opblock-section-header h4 { font-size: 14px; font-weight: 600; }
.swagger-ui .opblock-body { padding-bottom: 6px; }

/* ---------- Código (siempre oscuro: el resaltado de Swagger está pensado para fondo oscuro) ---------- */
.swagger-ui pre.microlight, .swagger-ui .highlight-code pre {
  background: var(--code-bg) !important; border-radius: 12px; padding: 14px 16px !important;
  font-size: 13px; line-height: 1.5;
}

/* ---------- Tablas, campos y botones ---------- */
.swagger-ui table tbody tr td, .swagger-ui table thead tr th { border-color: var(--sep); }
.swagger-ui input[type=text], .swagger-ui input[type=password], .swagger-ui input[type=search],
.swagger-ui select, .swagger-ui textarea {
  background: var(--card); color: var(--label); border: 1px solid var(--sep-strong);
  border-radius: 10px; padding: 8px 12px; min-height: 36px; box-shadow: none;
}
.swagger-ui textarea { font-size: 13px; line-height: 1.5; }
.swagger-ui .btn { border-radius: 980px; padding: 7px 18px; font-weight: 600; box-shadow: none;
  background: transparent; color: var(--label); border: 1px solid var(--sep-strong); }
.swagger-ui .btn:hover { box-shadow: none; background: var(--fill); }
.swagger-ui .btn.execute { background: var(--btn); border-color: var(--btn); color: var(--on-btn); }
.swagger-ui .btn.execute:hover { background: var(--btn); filter: brightness(1.08); }
.swagger-ui .btn.cancel { color: var(--danger); border-color: var(--danger); }
.swagger-ui .btn-group .btn { border-radius: 980px; }
.swagger-ui .responses-inner { padding: 16px; }
.swagger-ui .model-box { background: var(--fill); border-radius: 10px; }
.swagger-ui section.models { border: 1px solid var(--sep); border-radius: 14px; }

/* ---------- Foco visible con teclado ---------- */
.swagger-ui :focus-visible { outline: 3px solid var(--link); outline-offset: 2px; border-radius: 8px; }
"""

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%F0%9F%9A%A8%3C/text%3E%3C/svg%3E"
)


def registrar_docs(app: FastAPI) -> None:
    """Reemplaza /docs por una versión de Swagger UI con el tema de SENTIR."""

    @app.get("/docs", include_in_schema=False)
    def docs_personalizado() -> HTMLResponse:
        base = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} · Documentación",
            swagger_favicon_url=FAVICON,
            swagger_ui_parameters={
                "docExpansion": "none",               # grupos colapsados: menos ruido
                "defaultModelsExpandDepth": -1,       # oculta la sección "Schemas"
                "displayRequestDuration": True,
                "tryItOutEnabled": True,              # el body ya es editable, sin clic extra
                "syntaxHighlight.theme": "agate",
            },
        )
        html = base.body.decode("utf-8").replace("</head>", f"<style>{CSS}</style></head>")
        return HTMLResponse(html)
