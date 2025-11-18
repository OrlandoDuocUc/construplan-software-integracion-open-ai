def global_stats(request):
    if not request.user.is_authenticated:
        return {}

    from models_core.models import ConstructionModel
    from analysis.models import AnalysisResult

    user_models = ConstructionModel.objects.filter(user=request.user)
    if request.user.is_staff:
        total_models = ConstructionModel.objects.count()
        total_results = AnalysisResult.objects.count()
    else:
        total_models = user_models.count()
        total_results = AnalysisResult.objects.filter(construction_model__user=request.user).count()

    return {
        'global_model_count': total_models,
        'global_results_count': total_results,
    }
