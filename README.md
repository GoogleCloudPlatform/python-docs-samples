<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Delete, allow, and manage cookies in Chrome</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background-color: #fff;
      color: #1f1f1f;
      line-height: 1.6;
      padding: 24px 16px;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    h1 {
      font-size: 2rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      margin-bottom: 0.25rem;
    }
    .subhead {
      font-size: 1rem;
      color: #3c4043;
      margin-bottom: 1.5rem;
    }
    hr {
      border: none;
      border-top: 1px solid #dadce0;
      margin: 1.5rem 0;
    }
    h2 {
      font-size: 1.5rem;
      font-weight: 500;
      margin: 1.5rem 0 0.5rem;
    }
    h3 {
      font-size: 1.2rem;
      font-weight: 500;
      margin: 1.25rem 0 0.25rem;
    }
    p, li {
      color: #202124;
      margin-bottom: 0.75rem;
    }
    ul, ol {
      padding-left: 1.5rem;
      margin-bottom: 1rem;
    }
    li {
      margin-bottom: 0.3rem;
    }
    .note, .tip {
      background-color: #f8f9fa;
      border-left: 4px solid #1a73e8;
      padding: 0.75rem 1rem;
      margin: 1rem 0;
      border-radius: 0 4px 4px 0;
    }
    .tip {
      border-left-color: #34a853;
    }
    .code-block {
      background: #f1f3f4;
      padding: 0.75rem 1rem;
      border-radius: 6px;
      font-family: 'Roboto Mono', 'Courier New', monospace;
      font-size: 0.9rem;
      overflow-x: auto;
      margin: 0.75rem 0;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .badge {
      display: inline-block;
      background: #e8eaed;
      padding: 0.1rem 0.6rem;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 500;
      color: #3c4043;
      margin-right: 0.3rem;
    }
    .device-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin: 1rem 0 0.5rem;
    }
    .device-tab {
      background: #e8eaed;
      padding: 0.3rem 1rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 500;
      color: #3c4043;
    }
    .device-tab.active {
      background: #1a73e8;
      color: white;
    }
    .step-list {
      list-style-type: decimal;
      padding-left: 1.5rem;
    }
    .step-list li {
      margin-bottom: 0.3rem;
    }
    .button-ghost {
      display: inline-block;
      background: #f1f3f4;
      padding: 0.1rem 0.6rem;
      border-radius: 4px;
      font-family: inherit;
      font-size: 0.9rem;
    }
    .toggle-row {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin: 0.5rem 0;
      flex-wrap: wrap;
    }
    .toggle-label {
      font-weight: 500;
      min-width: 140px;
    }
    .toggle-value {
      background: #e8eaed;
      padding: 0.1rem 0.8rem;
      border-radius: 12px;
      font-size: 0.8rem;
    }
    .footer-links {
      margin-top: 2.5rem;
      border-top: 1px solid #dadce0;
      padding-top: 1.5rem;
      display: flex;
      flex-wrap: wrap;
      gap: 1rem 2rem;
    }
    .footer-links a, .related a {
      color: #1a73e8;
      text-decoration: none;
    }
    .footer-links a:hover, .related a:hover {
      text-decoration: underline;
    }
    .related {
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid #dadce0;
    }
    .related h3 {
      margin-top: 0;
    }
    .feedback {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      margin: 2rem 0 0;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem 1.5rem;
    }
    .feedback span {
      font-weight: 500;
    }
    .feedback .btn-group {
      display: flex;
      gap: 0.75rem;
    }
    .feedback .btn-group button {
      background: none;
      border: 1px solid #dadce0;
      padding: 0.2rem 1.2rem;
      border-radius: 20px;
      font-size: 0.9rem;
      cursor: default;
      color: #3c4043;
    }
    .help-community {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      margin: 1rem 0;
    }
    .help-community p {
      margin-bottom: 0.25rem;
    }
    .help-community a {
      color: #1a73e8;
      text-decoration: none;
    }
    .help-community a:hover {
      text-decoration: underline;
    }
    @media (max-width: 480px) {
      h1 { font-size: 1.6rem; }
      .device-tabs { gap: 0.3rem; }
      .device-tab { font-size: 0.75rem; padding: 0.2rem 0.7rem; }
      .feedback { flex-direction: column; align-items: flex-start; }
    }
  </style>
</head>
<body>
<div class="container">
  <!-- header -->
  <h1>Delete, allow, and manage cookies in Chrome</h1>
  <p class="subhead">You can choose to delete existing cookies, allow or block third-party cookies, and set preferences for certain websites.</p>

  <!-- understand cookies -->
  <h2>Understand cookies</h2>
  <p>Cookies are files created by websites you visit. By saving information about your visit, they make your online experience easier. For example, sites can keep you signed in, remember your site preferences, and give you locally relevant content.</p>
  <p>There are 2 types of cookies:</p>
  <ul>
    <li><strong>First-party cookies:</strong> Created by the site you visit. The site is shown in the address bar.</li>
    <li><strong>Third-party cookies:</strong> Created by other sites. A site you visit can embed content from other sites, for example images, ads, and text. Any of these sites can use third-party cookies to personalize content and ads, and learn about actions you take on other sites.</li>
  </ul>
  <div class="tip">
    <strong>Tip:</strong> Some sites may prompt you to accept or reject cookies.
  </div>
  <p>There are other ways that sites can personalize content and ads. Features like ad topics and site-suggested ads in Chrome allow sites to show you personalized content. These features limit what sites and their partners can learn about you. <a href="#" style="color:#1a73e8;">Learn more about managing these features</a>.</p>

  <hr>

  <!-- device selector -->
  <div class="device-tabs">
    <span class="device-tab">Android</span>
    <span class="device-tab active">Computer</span>
    <span class="device-tab">iPhone &amp; iPad</span>
  </div>

  <!-- delete all cookies -->
  <h2>Delete all cookies</h2>
  <div class="note">
    <strong>Important:</strong> If you delete cookies, you may get signed out of sites that remember you. Your saved preferences can also be deleted. This applies whenever a cookie is deleted.
  </div>
  <ol class="step-list">
    <li>On your Android device, open Chrome <span class="badge">Chrome</span>.</li>
    <li>At the top right, tap <strong>More</strong> <span class="button-ghost">⋮</span> <strong>Settings</strong>.</li>
    <li>Tap <strong>Privacy and security</strong> &gt; <strong>Delete browsing data</strong>.</li>
    <li>Next to "Time range," from the dropdown menu, choose the browsing data time range you want to delete:
      <ul>
        <li>Last 15 minutes</li>
        <li>Last hour</li>
        <li>Last 24 hours</li>
        <li>Last 7 days</li>
        <li>Last 4 weeks</li>
        <li>All time</li>
      </ul>
    </li>
    <li>Check <strong>Cookies and site data</strong>.</li>
    <li>Check other items you want to delete.</li>
    <li>To confirm, tap <strong>Delete data</strong>.</li>
  </ol>

  <!-- delete single site -->
  <h2>Delete cookies from a single site</h2>
  <ol class="step-list">
    <li>On your Android device, open Chrome <span class="badge">Chrome</span>.</li>
    <li>Go to a website.</li>
    <li>At the top left of the address bar, tap <strong>Page info</strong> <span class="button-ghost">🔒</span> &gt; <strong>Cookies and site data</strong>.</li>
    <li>Next to the stored data, tap <strong>Delete</strong> <span class="button-ghost">🗑️</span>.</li>
  </ol>

  <hr>

  <!-- third-party settings -->
  <h2>Change your third-party cookie settings</h2>
  <h3>Allow or block third-party cookies</h3>
  <h3>Allow third-party cookies for a specific site</h3>
  <h3>Allow third-party cookies temporarily for a specific site</h3>
  <p>If you block third-party cookies, some sites may not work as you expected. You can temporarily allow third-party cookies for a specific site you visit.</p>
  <ol class="step-list">
    <li>On your Android device, open Chrome <span class="badge">Chrome</span>.</li>
    <li>In the address bar, at the top left:
      <ul>
        <li><strong>To allow third-party cookies:</strong> Tap <strong>Page info</strong> <span class="button-ghost">🔒</span> &gt; <strong>Cookies and site data</strong> and turn on <strong>Third-party cookies</strong>.</li>
        <li><strong>To block third-party cookies:</strong> Tap <strong>Page info</strong> <span class="button-ghost">🔒</span> &gt; <strong>Cookies and site data</strong> and turn off <strong>Third-party cookies</strong>.</li>
      </ul>
    </li>
  </ol>
  <div class="tip">
    <strong>Tips:</strong>
    <ul>
      <li>This option is only temporary and only for the site you’re on.</li>
      <li>Sites get added to the exception list automatically.</li>
      <li>If you temporarily allow third-party cookies on a site, that setting carries over into Incognito mode and you can't reset it from Incognito mode.</li>
    </ul>
  </div>

  <!-- related sites -->
  <h2>Allow related sites to access your activity</h2>
  <p>A company can define a group of sites that are related to each other. For example, a company might want to keep you signed in as you move between acme-music.example and acme-video.example.</p>
  <ul>
    <li><strong>If you allow third-party cookies:</strong> Allows related sites to access your activity to personalize content or keep you signed in across sites.</li>
    <li><strong>If you block third-party cookies:</strong> It often prevents this kind of connection between sites. You can block third-party cookies while you allow sites in the same group to improve your experience.</li>
  </ul>
  <p>You can find the full list of companies who define groups of related sites on <a href="#" style="color:#1a73e8;">Github</a>. Learn more about <a href="#" style="color:#1a73e8;">related sites and third-party cookies</a>.</p>
  <p><strong>To allow related sites to find your activity within the group:</strong></p>
  <ol class="step-list">
    <li>On your Android device, open Chrome <span class="badge">Chrome</span>.</li>
    <li>At the top right, tap <strong>More</strong> <span class="button-ghost">⋮</span> <strong>Settings</strong>.</li>
    <li>Tap <strong>Privacy and security</strong> &gt; <strong>Third-party cookies</strong> &gt; <strong>Block third-party cookies</strong>.</li>
    <li>Tap the arrow next to "Block third-party cookies."</li>
    <li>Turn <strong>Allow related sites to see your activity in the group</strong> on or off.</li>
  </ol>
  <p><strong>To show related sites in the same group:</strong></p>
  <ol class="step-list">
    <li>On your Android device, open Chrome <span class="badge">Chrome</span>.</li>
    <li>At the top right, tap <strong>More</strong> <span class="button-ghost">⋮</span> <strong>Settings</strong>.</li>
    <li>Tap <strong>Site settings</strong> &gt; <strong>All sites</strong>.</li>
    <li>Choose a site.</li>
    <li>Under “Sites under [website link],” find sites in the same group.</li>
  </ol>

  <hr>

  <!-- related resources -->
  <div class="related">
    <h3>Related resources</h3>
    <ul>
      <li><a href="#">Change site settings permissions</a></li>
      <li><a href="#">Delete browsing data in Chrome</a></li>
      <li><a href="#">Clear cache &amp; cookies</a></li>
      <li><a href="#">Manage your ad privacy in Chrome</a></li>
      <li><a href="#">Learn about on-device site data in Chrome</a></li>
    </ul>
  </div>

  <!-- feedback -->
  <div class="feedback">
    <span>Give feedback about this article</span>
    <span>Was this helpful?</span>
    <div class="btn-group">
      <button>Yes</button>
      <button>No</button>
    </div>
  </div>

  <!-- need more help -->
  <div class="help-community">
    <p><strong>Need more help?</strong></p>
    <p>Try these next steps:</p>
    <p><a href="#">Post to the help community</a> &nbsp; Get answers from community members</p>
  </div>

  <!-- footer / language -->
  <div class="footer-links">
    <a href="#">Help</a>
    <a href="#">Delete browsing data in Chrome</a>
    <a href="#">Export your data from Chrome</a>
    <a href="#">Check or delete your Chrome browsing history</a>
    <a href="#">Delete, allow, and manage cookies in Chrome</a>
    <a href="#">Manage passwords in Chrome</a>
    <a href="#">Reset Chrome settings to default</a>
    <a href="#">Learn about on-device site data in Chrome</a>
    <span style="color:#3c4043; margin-left: auto;">Language</span>
  </div>
</div>
</body>
</html>
