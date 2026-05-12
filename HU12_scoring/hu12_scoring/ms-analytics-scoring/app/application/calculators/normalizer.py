from typing import Dict, List

class Normalizer:
    """
    Normalizes indicator values to 0-1 scale.
    Follows SRP: only handles normalization logic.
    """

    @staticmethod
    def min_max(value: float, min_val: float, max_val: float) -> float:
        """
        Apply Min-Max normalization.

        Args:
            value (float): Raw value.
            min_val (float): Minimum reference value.
            max_val (float): Maximum reference value.

        Returns:
            float: Normalized value 0.0 to 1.0.
        """
        if max_val == min_val:
            return 0.0
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))

    @staticmethod
    def normalize_indicators(
        indicators: List[Dict[str, float]],
        keys: List[str],
    ) -> List[Dict[str, float]]:
        """
        Normalize a list of indicator dictionaries.

        Args:
            indicators (List[Dict]): Raw indicator values.
            keys (List[str]): Keys to normalize.

        Returns:
            List[Dict]: Normalized indicators.
        """
        result = []
        for key in keys:
            values = [ind[key] for ind in indicators if key in ind]
            if not values:
                continue
            min_val = min(values)
            max_val = max(values)
            for ind in indicators:
                if key in ind:
                    ind[f"{key}_norm"] = Normalizer.min_max(
                        ind[key], min_val, max_val
                    )
        return indicators
