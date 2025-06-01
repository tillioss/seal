"""Tests for app.schemas.base module."""

import pytest
from pydantic import ValidationError

from app.schemas.base import (
    EMTScores, ClassMetadata, InterventionRequest,
    InterventionStrategy, SuccessMetrics, InterventionPlan,
    HealthResponse
)


class TestEMTScores:
    """Test cases for EMTScores schema."""

    def test_valid_emt_scores(self, sample_emt_scores):
        """Test valid EMT scores creation."""
        scores = EMTScores(**sample_emt_scores)
        assert scores.EMT1 == sample_emt_scores["EMT1"]
        assert scores.EMT2 == sample_emt_scores["EMT2"]
        assert scores.EMT3 == sample_emt_scores["EMT3"]
        assert scores.EMT4 == sample_emt_scores["EMT4"]

    def test_emt_scores_validation_valid_range(self):
        """Test EMT scores validation with valid range."""
        valid_scores = {
            "EMT1": [0.0, 50.0, 100.0],
            "EMT2": [25.0, 75.0],
            "EMT3": [100.0],
            "EMT4": [0.0, 100.0]
        }
        scores = EMTScores(**valid_scores)
        assert scores.EMT1 == [0.0, 50.0, 100.0]

    def test_emt_scores_validation_invalid_low(self):
        """Test EMT scores validation with scores below 0."""
        invalid_scores = {
            "EMT1": [-1.0, 50.0],
            "EMT2": [25.0, 75.0],
            "EMT3": [100.0],
            "EMT4": [0.0, 100.0]
        }
        with pytest.raises(ValidationError) as exc_info:
            EMTScores(**invalid_scores)
        assert "All scores must be between 0 and 100" in str(exc_info.value)

    def test_emt_scores_validation_invalid_high(self):
        """Test EMT scores validation with scores above 100."""
        invalid_scores = {
            "EMT1": [50.0, 101.0],
            "EMT2": [25.0, 75.0],
            "EMT3": [100.0],
            "EMT4": [0.0, 100.0]
        }
        with pytest.raises(ValidationError) as exc_info:
            EMTScores(**invalid_scores)
        assert "All scores must be between 0 and 100" in str(exc_info.value)

    def test_emt_scores_empty_list(self):
        """Test EMT scores with empty lists."""
        empty_scores = {
            "EMT1": [],
            "EMT2": [],
            "EMT3": [],
            "EMT4": []
        }
        scores = EMTScores(**empty_scores)
        assert scores.EMT1 == []


class TestClassMetadata:
    """Test cases for ClassMetadata schema."""

    def test_valid_class_metadata(self, sample_class_metadata):
        """Test valid class metadata creation."""
        metadata = ClassMetadata(**sample_class_metadata)
        assert metadata.class_id == sample_class_metadata["class_id"]
        assert metadata.deficient_area == sample_class_metadata["deficient_area"]
        assert metadata.num_students == sample_class_metadata["num_students"]

    def test_class_metadata_validation_positive_students(self):
        """Test class metadata validation with positive student count."""
        valid_metadata = {
            "class_id": "TEST_001",
            "deficient_area": "EMT1",
            "num_students": 1
        }
        metadata = ClassMetadata(**valid_metadata)
        assert metadata.num_students == 1

    def test_class_metadata_validation_zero_students(self):
        """Test class metadata validation with zero students."""
        invalid_metadata = {
            "class_id": "TEST_001",
            "deficient_area": "EMT1",
            "num_students": 0
        }
        with pytest.raises(ValidationError) as exc_info:
            ClassMetadata(**invalid_metadata)
        assert "ensure this value is greater than 0" in str(exc_info.value)

    def test_class_metadata_validation_negative_students(self):
        """Test class metadata validation with negative students."""
        invalid_metadata = {
            "class_id": "TEST_001",
            "deficient_area": "EMT1",
            "num_students": -5
        }
        with pytest.raises(ValidationError) as exc_info:
            ClassMetadata(**invalid_metadata)
        assert "ensure this value is greater than 0" in str(exc_info.value)

    def test_class_metadata_valid_deficient_areas(self):
        """Test class metadata with all valid deficient areas."""
        valid_areas = ["EMT1", "EMT2", "EMT3", "EMT4"]
        for area in valid_areas:
            metadata = ClassMetadata(
                class_id="TEST_001",
                deficient_area=area,
                num_students=25
            )
            assert metadata.deficient_area == area


class TestInterventionRequest:
    """Test cases for InterventionRequest schema."""

    def test_valid_intervention_request(self, sample_intervention_request):
        """Test valid intervention request creation."""
        assert isinstance(sample_intervention_request.scores, EMTScores)
        assert isinstance(sample_intervention_request.metadata, ClassMetadata)

    def test_intervention_request_with_custom_data(self):
        """Test intervention request with custom data."""
        scores = EMTScores(
            EMT1=[80.0], EMT2=[70.0], EMT3=[90.0], EMT4=[85.0]
        )
        metadata = ClassMetadata(
            class_id="CUSTOM_001",
            deficient_area="EMT3",
            num_students=15
        )
        request = InterventionRequest(scores=scores, metadata=metadata)
        assert request.scores.EMT1 == [80.0]
        assert request.metadata.class_id == "CUSTOM_001"


class TestInterventionStrategy:
    """Test cases for InterventionStrategy schema."""

    def test_valid_intervention_strategy(self):
        """Test valid intervention strategy creation."""
        strategy = InterventionStrategy(
            activity="Emotion Flashcards",
            implementation=["Step 1", "Step 2", "Step 3"],
            expected_outcomes=["Outcome 1", "Outcome 2"],
            time_allocation="30 minutes",
            resources=["Flashcards", "Timer"]
        )
        assert strategy.activity == "Emotion Flashcards"
        assert len(strategy.implementation) == 3
        assert len(strategy.expected_outcomes) == 2
        assert strategy.time_allocation == "30 minutes"
        assert len(strategy.resources) == 2

    def test_intervention_strategy_empty_lists(self):
        """Test intervention strategy with empty lists."""
        strategy = InterventionStrategy(
            activity="Test Activity",
            implementation=[],
            expected_outcomes=[],
            time_allocation="0 minutes",
            resources=[]
        )
        assert strategy.implementation == []
        assert strategy.expected_outcomes == []
        assert strategy.resources == []


class TestSuccessMetrics:
    """Test cases for SuccessMetrics schema."""

    def test_valid_success_metrics(self):
        """Test valid success metrics creation."""
        metrics = SuccessMetrics(
            quantitative=["15% improvement", "90% accuracy"],
            qualitative=["Increased confidence", "Better engagement"],
            assessment_methods=["Weekly tests", "Observations"]
        )
        assert len(metrics.quantitative) == 2
        assert len(metrics.qualitative) == 2
        assert len(metrics.assessment_methods) == 2

    def test_success_metrics_empty_lists(self):
        """Test success metrics with empty lists."""
        metrics = SuccessMetrics(
            quantitative=[],
            qualitative=[],
            assessment_methods=[]
        )
        assert metrics.quantitative == []
        assert metrics.qualitative == []
        assert metrics.assessment_methods == []


class TestInterventionPlan:
    """Test cases for InterventionPlan schema."""

    def test_valid_intervention_plan(self):
        """Test valid intervention plan creation."""
        strategy = InterventionStrategy(
            activity="Test Activity",
            implementation=["Step 1"],
            expected_outcomes=["Outcome 1"],
            time_allocation="30 minutes",
            resources=["Resource 1"]
        )
        metrics = SuccessMetrics(
            quantitative=["15% improvement"],
            qualitative=["Better engagement"],
            assessment_methods=["Weekly tests"]
        )
        plan = InterventionPlan(
            analysis="Test analysis",
            strategies=[strategy],
            timeline={"week1": ["Activity 1"], "week2": ["Activity 2"]},
            success_metrics=metrics
        )
        assert plan.analysis == "Test analysis"
        assert len(plan.strategies) == 1
        assert "week1" in plan.timeline
        assert isinstance(plan.success_metrics, SuccessMetrics)

    def test_intervention_plan_min_strategies(self):
        """Test intervention plan with minimum strategies."""
        strategy = InterventionStrategy(
            activity="Single Activity",
            implementation=["Step 1"],
            expected_outcomes=["Outcome 1"],
            time_allocation="30 minutes",
            resources=["Resource 1"]
        )
        metrics = SuccessMetrics(
            quantitative=[], qualitative=[], assessment_methods=[]
        )
        plan = InterventionPlan(
            analysis="Minimal plan",
            strategies=[strategy],
            timeline={},
            success_metrics=metrics
        )
        assert len(plan.strategies) == 1

    def test_intervention_plan_max_strategies(self):
        """Test intervention plan with maximum strategies."""
        strategies = []
        for i in range(5):  # Max 5 strategies
            strategy = InterventionStrategy(
                activity=f"Activity {i+1}",
                implementation=[f"Step {i+1}"],
                expected_outcomes=[f"Outcome {i+1}"],
                time_allocation="30 minutes",
                resources=[f"Resource {i+1}"]
            )
            strategies.append(strategy)
        
        metrics = SuccessMetrics(
            quantitative=[], qualitative=[], assessment_methods=[]
        )
        plan = InterventionPlan(
            analysis="Maximum strategies plan",
            strategies=strategies,
            timeline={},
            success_metrics=metrics
        )
        assert len(plan.strategies) == 5

    def test_intervention_plan_validation_no_strategies(self):
        """Test intervention plan validation with no strategies."""
        metrics = SuccessMetrics(
            quantitative=[], qualitative=[], assessment_methods=[]
        )
        with pytest.raises(ValidationError) as exc_info:
            InterventionPlan(
                analysis="No strategies plan",
                strategies=[],
                timeline={},
                success_metrics=metrics
            )
        assert "ensure this value has at least 1 items" in str(exc_info.value)

    def test_intervention_plan_validation_too_many_strategies(self):
        """Test intervention plan validation with too many strategies."""
        strategies = []
        for i in range(6):  # More than max 5 strategies
            strategy = InterventionStrategy(
                activity=f"Activity {i+1}",
                implementation=[f"Step {i+1}"],
                expected_outcomes=[f"Outcome {i+1}"],
                time_allocation="30 minutes",
                resources=[f"Resource {i+1}"]
            )
            strategies.append(strategy)
        
        metrics = SuccessMetrics(
            quantitative=[], qualitative=[], assessment_methods=[]
        )
        with pytest.raises(ValidationError) as exc_info:
            InterventionPlan(
                analysis="Too many strategies plan",
                strategies=strategies,
                timeline={},
                success_metrics=metrics
            )
        assert "ensure this value has at most 5 items" in str(exc_info.value)


class TestHealthResponse:
    """Test cases for HealthResponse schema."""

    def test_valid_health_response(self):
        """Test valid health response creation."""
        response = HealthResponse(
            status="healthy",
            version="1.0.0",
            llm_provider="gemini"
        )
        assert response.status == "healthy"
        assert response.version == "1.0.0"
        assert response.llm_provider == "gemini"

    def test_health_response_different_statuses(self):
        """Test health response with different statuses."""
        statuses = ["healthy", "unhealthy", "degraded"]
        for status in statuses:
            response = HealthResponse(
                status=status,
                version="1.0.0",
                llm_provider="gemini"
            )
            assert response.status == status

    def test_health_response_different_providers(self):
        """Test health response with different providers."""
        providers = ["gemini", "openai", "claude"]
        for provider in providers:
            response = HealthResponse(
                status="healthy",
                version="1.0.0",
                llm_provider=provider
            )
            assert response.llm_provider == provider 