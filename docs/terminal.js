document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('warning-modal');
  const acceptBtn = document.getElementById('accept-risk-btn');
  const terminal = document.getElementById('terminal-container');
  const bootSeq = document.getElementById('boot-sequence');
  const feed = document.getElementById('feed');
  const nameInput = document.getElementById('user-name-input');
  const postLogin = document.getElementById('post-login-content');
  const displayName = document.getElementById('display-name');
  const forkCount = document.getElementById('fork-count');
  const nameEntryBlock = document.getElementById('name-entry-block');

  // 1. WARNING MODAL / CONSENT
  const hasAccepted = localStorage.getItem('dca_warning_accepted');

  if (hasAccepted) {
    modal.style.display = 'none';
    terminal.classList.remove('hidden');
    bootSeq.style.display = 'none';
    feed.classList.remove('hidden');
    checkPersistence();
  } else {
    acceptBtn.addEventListener('click', () => {
      localStorage.setItem('dca_warning_accepted', 'true');
      modal.style.display = 'none';
      terminal.classList.remove('hidden');
      runBootSequence();
    });
  }

  // 2. BOOT SEQUENCE (simple fade-in of lines)
  function runBootSequence() {
    const logs = bootSeq.querySelectorAll('.log');
    let delay = 0;
    logs.forEach((log) => {
      setTimeout(() => {
        log.style.opacity = 1;
      }, delay);
      delay += 500;
    });

    setTimeout(() => {
      bootSeq.style.display = 'none';
      feed.classList.remove('hidden');
      checkPersistence();
    }, delay + 1000);
  }

  // 3. NAME PERSISTENCE
  function checkPersistence() {
    const savedName = localStorage.getItem('bridge_name');
    if (savedName) {
      nameEntryBlock.style.display = 'none';
      displayName.textContent = savedName.toUpperCase();
      postLogin.classList.remove('hidden');
    } else if (nameInput) {
      nameInput.focus();
    }
  }

  if (nameInput) {
    nameInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        const name = nameInput.value.trim();
        if (name) {
          localStorage.setItem('bridge_name', name);
          displayName.textContent = name.toUpperCase();
          nameEntryBlock.style.display = 'none';
          postLogin.classList.remove('hidden');
        }
      }
    });
  }

  // 4. LIVE FORK COUNT (GitHub API)
  if (forkCount) {
    fetch('https://api.github.com/repos/steviesonz/digital-collective-atlas')
      .then(response => response.json())
      .then(data => {
        forkCount.textContent = data.forks_count ?? '0';
      })
      .catch(() => {
        forkCount.textContent = 'ERR';
      });
  }
});
