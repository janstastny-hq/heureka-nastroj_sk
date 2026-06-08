import streamlit as st
import sys
import os

from hledat_kategorie import HeurekaAllInOne

st.set_page_config(
    page_title="Heureka All-In-One SK",
    page_icon="🤖",
    layout="centered"
)

def nacti_nastroj():
    return HeurekaAllInOne()

nastroj = nacti_nastroj()

jazyk = st.radio(
    "🌐 Language / Jazyk:",
    options=["SK", "EN"],
    horizontal=True
)

txt = {
    "title": "🤖 Heureka All-In-One SK",
    "subtitle": "Inteligentné vyhľadávanie kategórií a systémových pravidiel" if jazyk == "SK" else "Smart search for categories and system rules",
    "desc": "Zadajte názov produktu z e-shopu a algoritmus se postará o zvyšok." if jazyk == "SK" else "Enter the product name from the e-shop and the algorithm will do the rest.",
    # 🌟 OPRAVA: Text nad vyhledávacím políčkem úplně nahoře
    "input_label": "📝 Obecný názov produktu:" if jazyk == "SK" else "📝 General product name:",
    "input_placeholder": "Zadejte názov produktu..." if jazyk == "SK" else "Enter product name...",
    "type_classic": "🔍 Typ vyhľadávania: Klasická zhoda" if jazyk == "SK" else "🔍 Search type: Classic match",
    "select_label": "👉 Vyberte alebo potvrďte finálnu kategóriu:" if jazyk == "SK" else "👉 Select or confirm the final category:",
    "rules_title": "### 📋 Systémové pravidlá pre:" if jazyk == "SK" else "### 📋 System rules for:",
    "structure_label": "**Správna štruktúra názvu:**" if jazyk == "SK" else "**Correct name structure:**",
    "no_rule": "Pre túto kategóriu nie je definované žiadne špecifické pravidlo v pravidla_sk.txt." if jazyk == "SK" else "No specific rule is defined for this category in pravidla_sk.txt.",
    "params_label": "🚨 **Povinné parametre v XML štruktúre:**" if jazyk == "SK" else "🚨 **Required parameters in XML structure:**",
    "no_param": "Pri tejto kategórii nie je vyžadovaný žiadny povinný parameter." if jazyk == "SK" else "No required parameter is specified for this category.",
    "err_relevant": "❌ Nepodarilo se nájsť žiadnu dostatečne relevantnú kategóriu. Skúste všeobecnejší názov." if jazyk == "SK" else "❌ No sufficiently relevant category found. Try a more general name.",
    "err_empty": "❌ Nepodarilo sa nájsť žiadnu zodpovedajúcu kategóriu." if jazyk == "SK" else "❌ No matching category found.",
    "all_params_label": "💡 **Odporúčané a volitelné parametre (Heureka V2):**" if jazyk == "SK" else "💡 **Recommended and optional parameters (Heureka V2):**",
    # 🌟 OPRAVA: Záhlaví uvnitř tabulky parametrů
    "table_header": "Názov parametra" if jazyk == "SK" else "Parameter name",
    "no_all_param": "Pre túto kategóriu nie sú v Heureka V2 definované žiadne ďalšie odporúčané parametre." if jazyk == "SK" else "No additional recommended parameters are defined for this category in Heureka V2.",
    # Texty pre modul hodnotenia
    "rating_title": "### ⭐ Ohodnoťte náš nástroj" if jazyk == "SK" else "### ⭐ Rate our tool",
    "rating_comment_label": "Máte pre nás odkaz alebo nápad na zlepšenie?" if jazyk == "SK" else "Do you have a message or an idea for improvement?",
    "rating_comment_placeholder": "Napíšte nám..." if jazyk == "SK" else "Write to us...",
    "rating_button": "Odoslať hodnotenie" if jazyk == "SK" else "Submit rating",
    "rating_success": "🎉 Ďakujeme! Vaše hodnotenie bolo úspešne uložené." if jazyk == "SK" else "🎉 Thank you! Your rating has been successfully saved.",
    "rating_warning": "Prosím, vyberte najskôr počet hviezdičiek." if jazyk == "SK" else "Please select a star rating first.",
    # Správcovské texty
    "admin_panel_title": "📊 Správa nástroja" if jazyk == "SK" else "📊 Tool Administration",
    "admin_password_label": "Zadajte správcovské heslo:" if jazyk == "SK" else "Enter admin password:",
    "admin_wrong_password": "❌ Nesprávne heslo!" if jazyk == "SK" else "❌ Incorrect password!"
}

st.title(txt["title"])
st.subheader(txt["subtitle"])
st.write(txt["desc"])

st.divider()

produkt_input = st.text_input(txt["input_label"], placeholder=txt["input_placeholder"])

if produkt_input.strip():
    shody = nastroj.vyhledej_presnou_logikou(produkt_input.strip())
    
    if shody:
        st.info(txt["type_classic"])
        
        relevantni_shody = [s for s in shody if s.get('shody', 0) >= 20]
        top_shody = relevantni_shody[:10]
        
        if top_shody:
            seznam_kategorii = [shoda['cesta'] for shoda in top_shody]
            vybrana_cesta = st.selectbox(txt["select_label"], seznam_kategorii)
            
            if vybrana_cesta:
                st.divider()
                koncova_kat = vybrana_cesta.split('|')[-1].strip()
                
                pravidlo_text = nastroj.najdi_nejlepsi_shodu_v_db(koncova_kat.lower(), nastroj.pravidla_db)
                parametry_text = nastroj.najdi_nejlepsi_shodu_v_db(koncova_kat.lower(), nastroj.parametry_db)
                vsechny_parametry_text = nastroj.najdi_nejlepsi_shodu_v_db(koncova_kat.lower(), nastroj.vsechny_parametry_db)
                
                st.markdown(f"{txt['rules_title']} `{koncova_kat}`")
                
                if pravidlo_text:
                    st.warning(f"{txt['structure_label']} {pravidlo_text}")
                else:
                    st.info(txt["no_rule"])
                
                if parametry_text and parametry_text.strip():
                    st.error(txt["params_label"])
                    
                    for param in parametry_text.split(','):
                        p_cisty = param.strip()
                        if not p_cisty:
                            continue
                        
                        p_lower = p_cisty.lower()
                        priklad_hodnoty = "Hodnota" if jazyk == "SK" else "Value"
                        
                        if "objem" in p_lower or "volume" in p_lower:
                            priklad_hodnoty = "500 ml"
                        elif "veľkosť" in p_lower or "velkost" in p_lower or "size" in p_lower:
                            priklad_hodnoty = "L"
                        elif "farba" in p_lower or "color" in p_lower or "colour" in p_lower:
                            priklad_hodnoty = "Čierna" if jazyk == "SK" else "Black"
                        elif "váha" in p_lower or "hmotnosť" in p_lower or "hmotnost" in p_lower or "weight" in p_lower:
                            priklad_hodnoty = "1.5 kg"
                        elif "materiál" in p_lower or "material" in p_lower:
                            priklad_hodnoty = "Bavlna" if jazyk == "SK" else "Cotton"
                        elif "šírka" in p_lower or "sirka" in p_lower or "width" in p_lower or "výška" in p_lower or "vyska" in p_lower or "height" in p_lower:
                            priklad_hodnoty = "60 cm"
                        
                        xml_ukazka = f"""```xml
<PARAM>
  <PARAM_NAME>{p_cisty}</PARAM_NAME>
  <VAL>{priklad_hodnoty}</VAL>
</PARAM>
```"""
                        st.markdown(f"**{p_cisty}:**")
                        st.markdown(xml_ukazka)
                else:
                    st.success(txt["no_param"])
                
                # --- NOVÝ IDENTICKÝ CZ VIZUÁL BEZ NUTNOSTI NUMPY (ŘAZENÝ ABECEDNĚ) ---
                st.write("")  
                st.info(txt["all_params_label"])
                
                if vsechny_parametry_text and vsechny_parametry_text.strip():
                    list_parametru = sorted([p.strip() for p in vsechny_parametry_text.split(',') if p.strip()])
                    
                    data_pro_tabulku = [{txt["table_header"]: param} for param in list_parametru]
                    
                    st.dataframe(
                        data_pro_tabulku,
                        use_container_width=True,
                        height=380,
                        hide_index=True
                    )
                else:
                    st.caption(txt["no_all_param"])
                        
        else:
            st.error(txt["err_relevant"])
    else:
        st.error(txt["err_empty"])

# ===============================================================================
# ⭐ MODUL PRE HODNOTENIE NÁSTROJA
# ===============================================================================
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    st.write(txt["rating_title"])
    SOUBOR_HODNOCENI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historie_hodnoceni.txt")

    with st.form("formular_hodnoceni_sk", clear_on_submit=True):
        hodnoceni = st.feedback("stars", key="kliknute_hvezdicky_sk")
        
        komentar = st.text_area(
            txt["rating_comment_label"], 
            placeholder=txt["rating_comment_placeholder"],
            key="kliknuty_komentar_sk"
        )
        
        odeslano = st.form_submit_button(txt["rating_button"])
        
        if odeslano:
            if hodnoceni is not None:
                pocet_hvezdicek = hodnoceni + 1
                hvezdy_text = "⭐" * pocet_hvezdicek + f" ({pocet_hvezdicek}/5)"
                
                cisty_komentar = komentar.strip() if komentar.strip() else "Bez textového komentára."
                radek_k_zapisu = f"Hodnotenie: {hvezdy_text} | Jazyk: {jazyk} | Vzkaz: {cisty_komentar}\n"
                
                try:
                    with open(SOUBOR_HODNOCENI, "a", encoding="utf-8") as f:
                        f.write(radek_k_zapisu)
                    st.success(txt["rating_success"])
                except Exception as e:
                    st.error(f"Chyba pri ukladaní: {e}")
            else:
                st.warning(txt["rating_warning"])

# 📊 ANONYMNÝ SKRYTÝ ROZBALOVACÍ PANEL ZABEZPEČENÝ HESLOM
st.write("")
with st.expander(txt["admin_panel_title"]):
    heslo = st.text_input(txt["admin_password_label"], type="password", key="sprava_heslo_sk")
    
    if heslo == "Bandyta12":
        if os.path.exists(SOUBOR_HODNOCENI):
            try:
                with open(SOUBOR_HODNOCENI, "r", encoding="utf-8") as f:
                    zaznamy = f.readlines()
                
                if zaznamy:
                    st.write(f"### 📋 Získané hodnotenia (Celkom: {len(zaznamy)}):")
                    for zr in reversed(zaznamy):
                        if zr.strip():
                            st.code(zr.strip(), language="text")
                else:
                    st.info("História hodnotení je zatiaľ prázdna.")
            except Exception as e:
                st.error(f"Chyba pri čítaní: {e}")
        else:
            st.info("Zatiaľ nikto neodoslal žiadne hodnotenie.")
    elif heslo != "":
        st.error(txt["admin_wrong_password"])