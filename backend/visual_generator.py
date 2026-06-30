import io
import base64
import textwrap
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_concept_visual(title: str, explanation_text: str, subject: str = "science") -> str:
    """
    Create a highly visual, child-friendly concept summary card using matplotlib in a dark theme.
    Splits layout into two halves: left side displays key points; right side displays a dynamic diagrammatic illustration.
    """
    fig, ax = plt.subplots(figsize=(9.5, 5.5), facecolor='#1a2332')
    ax.set_facecolor('#1a2332')
    
    # Remove axis lines and ticks
    ax.axis('off')
    
    # Draw outer card border
    border_color = '#4da6ff' if subject.lower() == 'science' else '#ff9933'
    rect = patches.FancyBboxPatch(
        (0.015, 0.03), 0.97, 0.94,
        boxstyle="round,pad=0.01,rounding_size=0.03",
        linewidth=2.5,
        edgecolor=border_color,
        facecolor='#111a2e',
        transform=ax.transAxes
    )
    ax.add_patch(rect)
    
    # Subject Badge Header
    subj_title = f"CLASS 10 {subject.upper()} - DIGITAL SMART BOARD CARD"
    ax.text(
        0.04, 0.89, subj_title,
        transform=ax.transAxes,
        color='#4da6ff' if subject.lower() == 'science' else '#ff9933',
        fontsize=11,
        fontweight='bold',
        family='sans-serif'
    )
    
    # Title / Query Header
    wrapped_title = textwrap.fill(title, width=38)
    ax.text(
        0.04, 0.81, f"Topic: {wrapped_title}",
        transform=ax.transAxes,
        color='#ffffff',
        fontsize=14,
        fontweight='bold',
        family='sans-serif',
        va='top'
    )
    
    # Left Side: Key Takeaways (x from 0.04 to 0.50)
    clean_lines = [line.strip() for line in explanation_text.split('\n') if line.strip() and not line.startswith('**')]
    summary_bullets = []
    for l in clean_lines:
        # Strip markdown symbols
        clean_l = l.replace("*", "").replace("#", "").strip()
        # Skip markdown dividers
        if clean_l.startswith('==') or clean_l.startswith('--') or clean_l.startswith('__') or clean_l.strip() in ['***', '---', '___']:
            continue
        if len(clean_l) > 10 and not clean_l.startswith('Namaste') and not clean_l.startswith('Bhai/Beta'):
            summary_bullets.append(clean_l)
        if len(summary_bullets) >= 3:
            break
            
    if not summary_bullets:
        summary_bullets = [
            "Understand the core properties and formulas from your NCERT book.",
            "Connect these concepts to everyday experiments and situations.",
            "Solve numerical tasks and draw clean diagrams in exams."
        ]
        
    y_pos = 0.58
    ax.text(
        0.04, y_pos, "Core Concepts to Remember:",
        transform=ax.transAxes,
        color='#ffd700',  # Yellow accent
        fontsize=12,
        fontweight='bold',
        family='sans-serif'
    )
    
    y_pos -= 0.07
    for idx, bullet in enumerate(summary_bullets):
        wrapped_bullet = textwrap.fill(bullet, width=42)
        # Draw small custom bullet indicator box
        indicator = patches.Rectangle(
            (0.04, y_pos - 0.01), 0.015, 0.02,
            facecolor='#ffd700', edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(indicator)
        
        ax.text(
            0.065, y_pos, wrapped_bullet,
            transform=ax.transAxes,
            color='#e2e8f0',
            fontsize=10.5,
            family='sans-serif',
            va='top',
            linespacing=1.2
        )
        y_pos -= (0.13 + (wrapped_bullet.count('\n') * 0.035))
        if y_pos < 0.14:
            break
            
    # Right Side: Dynamic Diagram Drawing (x from 0.52 to 0.95)
    title_lower = title.lower()
    
    # 1. Chemistry Diagram (Reactants -> Products)
    if "reaction" in title_lower or "equation" in title_lower or "chem" in title_lower or "acid" in title_lower or "base" in title_lower or "metal" in title_lower:
        # Draw Left Reactants Box
        r_box = patches.FancyBboxPatch(
            (0.53, 0.35), 0.16, 0.20,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor='#1e293b', edgecolor='#4da6ff', linewidth=1.5,
            transform=ax.transAxes
        )
        ax.add_patch(r_box)
        ax.text(0.61, 0.45, "Reactants", transform=ax.transAxes, color='#ffffff', fontsize=10, fontweight='bold', ha='center', va='center')
        
        # Draw Arrow
        ax.annotate(
            "Chemical Change",
            xy=(0.78, 0.45), xytext=(0.69, 0.45),
            xycoords=ax.transAxes, textcoords=ax.transAxes,
            arrowprops=dict(facecolor='#4da6ff', edgecolor='#4da6ff', width=3, headwidth=8, shrink=0.05),
            color='#ffd700', fontsize=8, ha='center', va='bottom'
        )
        
        # Draw Right Products Box
        p_box = patches.FancyBboxPatch(
            (0.79, 0.35), 0.16, 0.20,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor='#1e293b', edgecolor='#ffd700', linewidth=1.5,
            transform=ax.transAxes
        )
        ax.add_patch(p_box)
        ax.text(0.87, 0.45, "Products", transform=ax.transAxes, color='#ffffff', fontsize=10, fontweight='bold', ha='center', va='center')
        
    # 2. Trigonometry Diagram (Right Angled Triangle)
    elif "trig" in title_lower or "triangle" in title_lower or "height" in title_lower or "distance" in title_lower:
        # Plot triangle lines directly on data coordinates
        # Map transAxes coordinate to raw coordinates: we use a secondary axes or transform them
        # Let's draw using custom patches / line plots with transform=ax.transAxes
        x_coords = [0.58, 0.86, 0.86, 0.58]
        y_coords = [0.25, 0.25, 0.65, 0.25]
        ax.plot(x_coords, y_coords, color='#ff9933', linewidth=2.5, transform=ax.transAxes)
        
        # Draw right angle indicator
        ax.plot([0.83, 0.83, 0.86], [0.25, 0.28, 0.28], color='#ffffff', linewidth=1, transform=ax.transAxes)
        
        # Labels
        ax.text(0.72, 0.20, "Base", transform=ax.transAxes, color='#e2e8f0', fontsize=9.5, ha='center')
        ax.text(0.88, 0.45, "Opposite", transform=ax.transAxes, color='#e2e8f0', fontsize=9.5, va='center')
        ax.text(0.68, 0.48, "Hypotenuse", transform=ax.transAxes, color='#ffd700', fontsize=9.5, ha='right', va='bottom')
        ax.text(0.63, 0.27, "θ", transform=ax.transAxes, color='#ffd700', fontsize=12, fontweight='bold')
        
    # 3. Biology / Process Flowchart
    elif "respir" in title_lower or "life" in title_lower or "process" in title_lower or "nutri" in title_lower or "circulat" in title_lower:
        # Draw process steps vertically
        steps = [
            "1. Intake",
            "2. Breakdown",
            "3. Energy (ATP)"
        ]
        y_flows = [0.58, 0.40, 0.22]
        for step, y_f in zip(steps, y_flows):
            s_box = patches.FancyBboxPatch(
                (0.56, y_f), 0.32, 0.11,
                boxstyle="round,pad=0.005,rounding_size=0.015",
                facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5,
                transform=ax.transAxes
            )
            ax.add_patch(s_box)
            ax.text(0.72, y_f + 0.05, step, transform=ax.transAxes, color='#ffffff', fontsize=9.5, fontweight='bold', ha='center', va='center')
            
        # Down arrows
        ax.annotate("", xy=(0.72, 0.52), xytext=(0.72, 0.57),
                    arrowprops=dict(arrowstyle="->", color="#10b981", lw=2),
                    transform=ax.transAxes)
        ax.annotate("", xy=(0.72, 0.34), xytext=(0.72, 0.39),
                    arrowprops=dict(arrowstyle="->", color="#10b981", lw=2),
                    transform=ax.transAxes)

    # 4. Mathematics Real Number Line
    elif "number" in title_lower or "real" in title_lower or "arith" in title_lower or "coordinate" in title_lower:
        # Draw number line
        ax.plot([0.55, 0.91], [0.45, 0.45], color='#ff9933', linewidth=2.5, transform=ax.transAxes)
        # Arrow heads
        ax.annotate("", xy=(0.52, 0.45), xytext=(0.55, 0.45),
                    arrowprops=dict(arrowstyle="->", color="#ff9933", lw=2),
                    transform=ax.transAxes)
        ax.annotate("", xy=(0.94, 0.45), xytext=(0.91, 0.45),
                    arrowprops=dict(arrowstyle="->", color="#ff9933", lw=2),
                    transform=ax.transAxes)
        
        # Tic marks and numbers
        tics = [0.59, 0.67, 0.75, 0.83, 0.91]
        labels = ["-2", "-1", "0", "1", "2"]
        for t, label in zip(tics, labels):
            ax.plot([t, t], [0.43, 0.47], color='#ffffff', linewidth=1.5, transform=ax.transAxes)
            ax.text(t, 0.38, label, transform=ax.transAxes, color='#ffffff', fontsize=10, ha='center')
            
        ax.text(0.73, 0.54, "Real Number Line", transform=ax.transAxes, color='#ffd700', fontsize=11, fontweight='bold', ha='center')

    # 5. Default Mindmap Concept Box
    else:
        # Draw a beautiful central concept bubble linked to study components
        center = patches.Circle((0.74, 0.44), 0.12, facecolor='#1e293b', edgecolor='#ffd700', linewidth=2, transform=ax.transAxes)
        ax.add_patch(center)
        ax.text(0.74, 0.44, "Concept", transform=ax.transAxes, color='#ffd700', fontsize=10, fontweight='bold', ha='center', va='center')
        
        # Satellites
        sats = [
            ("Learn", 0.56, 0.62),
            ("Practice", 0.91, 0.44),
            ("Recall", 0.56, 0.26)
        ]
        for name, sx, sy in sats:
            sat_patch = patches.Circle((sx, sy), 0.065, facecolor='#2d3748', edgecolor='#e2e8f0', linewidth=1, transform=ax.transAxes)
            ax.add_patch(sat_patch)
            ax.text(sx, sy, name, transform=ax.transAxes, color='#ffffff', fontsize=8, ha='center', va='center')
            
            # Connective dashed lines
            ax.plot([0.74, sx], [0.44, sy], color='#8899a6', linestyle='--', linewidth=1, zorder=0, transform=ax.transAxes)
            
    # Footer
    ax.text(
        0.5, 0.08, "GuruAI Smart Board Teaching Assistant • Haryana Govt Schools",
        transform=ax.transAxes,
        color='#8899a6',
        fontsize=9,
        style='italic',
        ha='center'
    )
    
    plt.tight_layout()
    
    # Save figure to memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buffer.seek(0)
    
    # Encode as base64
    img_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"
