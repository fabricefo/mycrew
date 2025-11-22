import warnings
warnings.filterwarnings('ignore')
from rich import print # noqa: E402
from main_flow import BlogWritingFlow # noqa: E402


def main():
    """Main function using CrewAI Flow with input parameters and usage tracking"""
    
    # Get user inputs
    print("\n[bold yellow]🚀 Configuration de la création de blog[/bold yellow]")
    topic = input("Entrez le sujet de l'article: ") or "La difference entre Pulumi et Terraform"
    word_count = input("Entrez le nombre approximatif de mots: ") or "1200"
    read_time = input("Saisissez la durée de lecture approximative en minutes: ") or "8"
    
    print("\n[bold yellow]Démarrage du flux automatisé de création de blog[/bold yellow]")
    print(f"[bold cyan]Article: {topic}[/bold cyan]")
    print(f"[bold cyan]Cible: {word_count} words, {read_time} min read[/bold cyan]\n")
    
    # Create flow with inputs passed to constructor
    try:
        flow = BlogWritingFlow(topic=topic, word_count=word_count, read_time=read_time)
        result = flow.kickoff()
        
        print("\n" + "=" * 60)
        print("[bold green]🎉 FLUX DE CRÉATION DU BLOG TERMINÉ![/bold green]")
        print("=" * 60)
        print("[bold white]Resultat final:[/bold white]")
        print(result.get('final_output', 'No output generated'))
        print("=" * 60)
        
        # Display token usage metrics
        print("\n[bold blue]📊 METRIQUES D'USAGE[/bold blue]")
        print("=" * 40)
        
        # Get usage metrics from blog writing crew
        blog_crew = flow.blog_crew.crew()
        if hasattr(blog_crew, 'usage_metrics'):
            blog_metrics = blog_crew.usage_metrics
            print("[bold cyan]Phase de création de contenu:[/bold cyan]")
            print(f"  Total Tokens: {blog_metrics.total_tokens:,}")
            print(f"  Prompt Tokens: {blog_metrics.prompt_tokens:,}")
            print(f"  Completion Tokens: {blog_metrics.completion_tokens:,}")
            print(f"  Successful Requests: {blog_metrics.successful_requests}")
            if hasattr(blog_metrics, 'cached_prompt_tokens'):
                print(f"  Cached Prompt Tokens: {blog_metrics.cached_prompt_tokens:,}")
            print()
        
        # Calculate and display total metrics
        total_tokens = (blog_metrics.total_tokens if 'blog_metrics' in locals() else 0)
        total_requests = (blog_metrics.successful_requests if 'blog_metrics' in locals() else 0)
        
        print("[bold green]Overall Total:[/bold green]")
        print(f"  Combined Total Tokens: {total_tokens:,}")
        print(f"  Combined LLM Requests: {total_requests}")
        print("=" * 40)
        
    except Exception as e:
        print(f"\n[bold red]❌ Erreur lors de la création du blog: {e}[/bold red]")
        raise


if __name__ == "__main__":
    main()