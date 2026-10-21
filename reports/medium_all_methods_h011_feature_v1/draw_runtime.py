def draw(selected, filename, title, xmax, height):
    fig, ax = plt.subplots(figsize=(13, height), facecolor='white')
    fig.subplots_adjust(left=.33, right=.97, top=.82 if height < 7 else .89, bottom=.16 if height < 7 else .13)
    positions = np.arange(len(selected))
    values = np.array([r['pooled_map'] * 100 for r in selected])
    low = np.array([r['ci95_low'] * 100 for r in selected])
    high = np.array([r['ci95_high'] * 100 for r in selected])
    ax.barh(positions, values, height=.65,
            color=[colors.get(r['method'], '#9aa7b6') for r in selected], zorder=2)
    ax.errorbar(values, positions, xerr=[values - low, high - values],
                fmt='none', ecolor='#354254', capsize=3, linewidth=1.1, zorder=3)
    for y, r in zip(positions, selected):
        label = f"{r['pooled_map'] * 100:.4f}%".replace('.', ',')
        ax.text(xmax * .985, y, label, ha='right', va='center', fontsize=10,
                fontweight='bold' if r['method'] in colors else 'normal')
    ax.set(yticks=positions, yticklabels=[r['label'] for r in selected],
           xlim=(0, xmax), xlabel='Test MAP@12, % — среднее по всем 5519 наблюдениям')
    ax.invert_yaxis()
    ax.xaxis.grid(True, alpha=.18, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='y', length=0, pad=10)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
    fig.suptitle(title, fontsize=17, fontweight='bold', x=.04, ha='left', y=.975)
    fig.text(.04, .89 if height < 7 else .93,
             '3 временных фолда · 20 000 покупателей · каталог 10 000 товаров · seed 42', fontsize=10, color='#526071')
    fig.text(.04, .055 if height < 7 else .055,
             'Усы: 95% bootstrap по покупателям, 5000 повторов. Один seed; test-недели ранее просматривались.',
             fontsize=9, color='#526071')
    fig.text(.04, .02,
             'H011: лимит исследований повышен 40 → 300 во время поиска; равное число программ не означает равные расходы.',
             fontsize=9, color='#526071')
    fig.savefig(OUT / f'{filename}.png', dpi=180)
    fig.savefig(OUT / f'{filename}.svg')
    plt.close(fig)
