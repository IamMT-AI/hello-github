"""
Test Order Generation Script
Generates synthetic test orders for development and testing purposes.
"""

import json
import random
import time
from pathlib import Path
from typing import Dict, List, Any
import argparse


def generate_test_face_data() -> Dict[str, Any]:
    """Generate synthetic face image metadata"""
    return {
        "filename": f"face_{random.randint(1000, 9999)}.jpg",
        "dimensions": random.choice([(512, 512), (1024, 1024), (768, 768)]),
        "format": "JPEG",
        "file_size": random.randint(50000, 500000),  # 50KB to 500KB
        "face_detection_score": round(random.uniform(0.7, 0.98), 3),
        "quality_score": round(random.uniform(0.6, 0.95), 3),
    }


def generate_test_preferences() -> Dict[str, Any]:
    """Generate synthetic user preferences"""
    styles = ["cartoon", "anime", "realistic", "stylized", "cute"]
    body_templates = ["default", "superhero", "casual", "formal", "sporty"]
    colors = ["vibrant", "pastel", "monochrome", "warm", "cool"]

    return {
        "style": random.choice(styles),
        "body_template": random.choice(body_templates),
        "color_scheme": random.choice(colors),
        "size": random.choice(["small", "medium", "large"]),
        "material": random.choice(["PLA", "ABS", "PETG", "resin"]),
        "finish": random.choice(["matte", "glossy", "textured"]),
        "special_features": random.sample(
            ["LED_eyes", "movable_arms", "custom_base", "engraved_name"],
            k=random.randint(0, 2),
        ),
    }


def generate_test_order(order_id: int) -> Dict[str, Any]:
    """Generate a single test order"""
    statuses = [
        "pending",
        "processing",
        "stylizing",
        "fusing",
        "printing",
        "completed",
        "failed",
    ]
    priorities = ["low", "normal", "high", "urgent"]

    order = {
        "order_id": f"TEST_{order_id:06d}",
        "timestamp": time.time() - random.randint(0, 86400 * 30),  # Last 30 days
        "status": random.choice(statuses),
        "priority": random.choice(priorities),
        "customer": {
            "user_id": f"user_{random.randint(1000, 9999)}",
            "email": f"test.user.{random.randint(100, 999)}@example.com",
            "name": f"Test User {order_id}",
        },
        "face_data": generate_test_face_data(),
        "preferences": generate_test_preferences(),
        "processing": {
            "submitted_at": time.time() - random.randint(0, 86400 * 30),
            "started_at": None,
            "completed_at": None,
            "estimated_completion": None,
            "processing_time": None,
        },
        "quality_scores": {
            "face_similarity": round(random.uniform(0.6, 0.95), 3),
            "style_consistency": round(random.uniform(0.65, 0.92), 3),
            "overall_quality": round(random.uniform(0.7, 0.88), 3),
        }
        if random.random() > 0.3
        else None,  # 70% have quality scores
        "files": {
            "original_face": f"uploads/{order_id:06d}/original.jpg",
            "stylized_image": f"processed/{order_id:06d}/stylized.png",
            "fused_model": f"models/{order_id:06d}/figurine.obj",
            "print_file": f"prints/{order_id:06d}/figurine.gcode",
        },
        "cost": {
            "base_price": round(random.uniform(15.0, 45.0), 2),
            "options_cost": round(random.uniform(0.0, 15.0), 2),
            "shipping": round(random.uniform(3.0, 12.0), 2),
            "total": None,  # Will be calculated
        },
    }

    # Calculate total cost
    order["cost"]["total"] = round(
        order["cost"]["base_price"]
        + order["cost"]["options_cost"]
        + order["cost"]["shipping"],
        2,
    )

    # Set processing times based on status
    if order["status"] != "pending":
        order["processing"]["started_at"] = order["processing"][
            "submitted_at"
        ] + random.randint(60, 3600)

        if order["status"] == "completed":
            order["processing"]["completed_at"] = order["processing"][
                "started_at"
            ] + random.randint(1800, 21600)
            order["processing"]["processing_time"] = (
                order["processing"]["completed_at"] - order["processing"]["started_at"]
            )
        elif order["status"] != "failed":
            order["processing"]["estimated_completion"] = time.time() + random.randint(
                3600, 43200
            )

    return order


def generate_test_batch(count: int, output_file: Path = None) -> List[Dict[str, Any]]:
    """Generate a batch of test orders"""
    print(f"🔄 Generating {count} test orders...")

    orders = []
    for i in range(1, count + 1):
        order = generate_test_order(i)
        orders.append(order)

        if i % 100 == 0:
            print(f"   Generated {i}/{count} orders...")

    print(f"✅ Generated {count} test orders")

    # Save to file if specified
    if output_file:
        with open(output_file, "w") as f:
            json.dump(orders, f, indent=2)
        print(f"💾 Saved orders to {output_file}")

    return orders


def generate_summary_stats(orders: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics for the test orders"""
    total_orders = len(orders)

    # Status distribution
    status_counts = {}
    for order in orders:
        status = order["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    # Priority distribution
    priority_counts = {}
    for order in orders:
        priority = order["priority"]
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

    # Style preferences
    style_counts = {}
    for order in orders:
        style = order["preferences"]["style"]
        style_counts[style] = style_counts.get(style, 0) + 1

    # Calculate average costs
    total_cost = sum(order["cost"]["total"] for order in orders)
    avg_cost = total_cost / total_orders if total_orders > 0 else 0

    # Processing time stats (completed orders only)
    completed_orders = [
        o
        for o in orders
        if o["status"] == "completed" and o["processing"]["processing_time"]
    ]
    avg_processing_time = (
        sum(o["processing"]["processing_time"] for o in completed_orders)
        / len(completed_orders)
        if completed_orders
        else 0
    )

    return {
        "total_orders": total_orders,
        "status_distribution": status_counts,
        "priority_distribution": priority_counts,
        "style_preferences": style_counts,
        "financial": {
            "total_revenue": round(total_cost, 2),
            "average_order_value": round(avg_cost, 2),
            "completed_orders_value": round(
                sum(o["cost"]["total"] for o in orders if o["status"] == "completed"), 2
            ),
        },
        "performance": {
            "completed_orders": len(completed_orders),
            "completion_rate": round(len(completed_orders) / total_orders * 100, 1)
            if total_orders > 0
            else 0,
            "average_processing_time_seconds": round(avg_processing_time, 1),
            "average_processing_time_hours": round(avg_processing_time / 3600, 1),
        },
    }


def main():
    """Command-line interface for test order generation"""
    parser = argparse.ArgumentParser(description="Generate synthetic test orders")
    parser.add_argument(
        "--count", type=int, default=100, help="Number of test orders to generate"
    )
    parser.add_argument("--output", help="Output JSON file for orders")
    parser.add_argument("--stats", help="Output JSON file for summary statistics")

    args = parser.parse_args()

    # Generate orders
    output_path = Path(args.output) if args.output else None
    orders = generate_test_batch(args.count, output_path)

    # Generate and display statistics
    stats = generate_summary_stats(orders)

    print("\n📊 Order Statistics:")
    print(f"   Total Orders: {stats['total_orders']}")
    print(f"   Completion Rate: {stats['performance']['completion_rate']:.1f}%")
    print(f"   Average Order Value: ${stats['financial']['average_order_value']:.2f}")
    print(
        f"   Average Processing Time: {stats['performance']['average_processing_time_hours']:.1f} hours"
    )

    print("\n📈 Status Distribution:")
    for status, count in stats["status_distribution"].items():
        percentage = count / stats["total_orders"] * 100
        print(f"   {status}: {count} ({percentage:.1f}%)")

    # Save statistics if requested
    if args.stats:
        with open(args.stats, "w") as f:
            json.dump(stats, f, indent=2)
        print(f"\n💾 Statistics saved to {args.stats}")


if __name__ == "__main__":
    main()
