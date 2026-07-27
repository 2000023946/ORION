import subprocess
import os
import shutil
import time

from generate_comparision_report import main as create_full_report


RESULT_DIR = "baseline_results"

SCRIPT = "./run_load_test.sh"


TESTS = [
    (100, 20, "2m"),
    (250, 50, "2m"),
    (500, 100, "2m"),
    # (1000, 200, "2m"),
    # (2000, 300, "2m"),
]

def clean_results():

    if os.path.exists(RESULT_DIR):
        print("Removing old results...")
        shutil.rmtree(RESULT_DIR)

    os.makedirs(RESULT_DIR)

    print("Created baseline_results/")


def run_test(users, spawn_rate, runtime):

    print("\n" + "=" * 60)
    print(f"Starting {users} user test")
    print(f"Spawn Rate: {spawn_rate}")
    print(f"Runtime: {runtime}")
    print("=" * 60)


    start = time.time()


    result = subprocess.run(
        [
            SCRIPT,
            str(users),
            str(spawn_rate),
            runtime
        ]
    )


    elapsed = time.time() - start


    if result.returncode == 0:

        print(
            f"{users} users completed "
            f"({elapsed:.2f}s)"
        )

    else:

        print(
            f"{users} users FAILED"
        )



def main():

    clean_results()


    start = time.time()


    # Run load tests sequentially
    for users, spawn_rate, runtime in TESTS:

        run_test(
            users,
            spawn_rate,
            runtime
        )


        print("Cooldown 10 seconds...")
        time.sleep(10)



    print("\nAll load tests finished.")


    print("\nGenerating comparison report...")


    # Generate final dashboard
    create_full_report()

    

    total = time.time() - start


    print("\n" + "=" * 60)
    print(
        f"Finished everything in {total/60:.2f} minutes"
    )
    print("=" * 60)



if __name__ == "__main__":
    main()