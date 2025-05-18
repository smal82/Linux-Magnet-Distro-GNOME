# 🧲 Linux Magnet Distro GNOME

![Logo](https://raw.githubusercontent.com/smal82/Linux-Magnet-Distro-Gnome/main/io.github.smal82.LinuxMagnetDistro.png)

## 🚀 Cos'è Linux Magnet Distro GNOME?

**Linux Magnet Distro GNOME** è un'app desktop moderna, realizzata in Python+GTK, che funge da hub centrale per scoprire, scaricare e gestire le ISO delle principali distribuzioni Linux.  
L'obiettivo è rendere semplice e veloce provare nuove distro, restando sempre aggiornato sulle ultime novità dell'universo Linux!

---

## ✨ Funzionalità

- 🔍 **Esplora le distro:** Visualizza e cerca le principali distribuzioni Linux.
- 📰 **Feed aggiornati:** Leggi le ultime news e novità dal mondo open source grazie all'integrazione con feed RSS.
- ⬇️ **Download rapidi:** Scarica le ISO delle distribuzioni direttamente dall'app.
- 🎨 **Interfaccia GNOME moderna**, semplice e intuitiva.
- 🌐 **Open source**: codice trasparente e modificabile da chiunque.

---

## 🛠️ Installazione

### 1. **Dipendenze richieste**

- [Flatpak](https://flatpak.org/setup/) (consigliato per installare facilmente la versione sandboxata)
- [pip](https://pip.pypa.io/en/stable/installation/) (solo per sviluppo)
- Python 3.10+ (solo per sviluppo locale)

---

### 2. **Installazione semplice tramite Flatpak**

#### **A. Installa Flatpak (se non ce l'hai già)**

Su Ubuntu/Mint/Debian:
```sh
sudo apt update
sudo apt install flatpak
```

#### **B. Aggiungi il repository Flathub (se non già fatto):**
```sh
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

#### **C. Installa Linux Magnet Distro GNOME**
_(Non appena sarà disponibile su Flathub)_
```sh
flatpak install flathub io.github.smal82.LinuxMagnetDistro
```

#### **D. Avvia l'app**
```sh
flatpak run io.github.smal82.LinuxMagnetDistro
```

---

### 3. **Installazione per sviluppatori (build locale da sorgente)**

#### **Clona la repository**
```sh
git clone https://github.com/smal82/Linux-Magnet-Distro-Gnome.git
cd Linux-Magnet-Distro-Gnome
```

#### **Costruisci e installa la Flatpak localmente**
Assicurati di avere [org.gnome.Platform//46](https://flathub.org/apps/org.gnome.Platform) e [org.gnome.Sdk//46] installati:
```sh
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46
```

Costruisci e installa:
```sh
flatpak run --filesystem=$PWD org.flatpak.Builder --user --install --force-clean build-dir io.github.smal82.LinuxMagnetDistro.yml
```

Avvia:
```sh
flatpak run io.github.smal82.LinuxMagnetDistro
```

---

## 🤝 Contribuire

Le pull request sono benvenute!  
Proponi nuove funzioni, segnala bug, o migliora la documentazione — ogni contributo è apprezzato!

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **MIT**.  
Consulta il file [LICENSE](LICENSE) per i dettagli.

---

## 📬 Contatti

- Autore: [smal82](https://github.com/smal82)
- Apri una [issue](https://github.com/smal82/Linux-Magnet-Distro-Gnome/issues) per segnalare bug o suggerire miglioramenti.

---

**Buon divertimento con Linux Magnet Distro GNOME!** 🧲🐧
